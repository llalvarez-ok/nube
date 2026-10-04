//+------------------------------------------------------------------+
//|                                  RIC_Delta_Divergencias_EA.mq5   |
//|  REAL INVESTORS CLUB · EA basado en las divergencias de          |
//|  "RIC Delta Pro" (precio vs CVD) en M1, M3, M5 y M15.            |
//|                                                                  |
//|  Cada temporalidad opera de forma independiente:                 |
//|   - Divergencia ALCISTA confirmada  -> compra de esa TF.         |
//|   - Divergencia BAJISTA confirmada  -> venta de esa TF.          |
//|   - La posición de una TF se cierra con la primera divergencia   |
//|     contraria de ESA MISMA TF (y, opcionalmente, se da vuelta).  |
//|                                                                  |
//|  Cuentas hedging: una posición por TF (magic propio por TF).     |
//|  Cuentas netting / exchange: posiciones virtuales por TF; el EA  |
//|  ajusta la posición neta del símbolo a la suma de las virtuales. |
//|                                                                  |
//|  El delta es la misma aproximación del indicador (velas M1       |
//|  clasificadas como compradoras/vendedoras); en Forex/CFD el      |
//|  volumen es volumen de ticks. No es asesoramiento financiero.    |
//+------------------------------------------------------------------+
#property copyright "Real Investors Club"
#property version   "1.10"
#property description "Opera las divergencias precio/CVD de RIC Delta Pro en M1, M3, M5 y M15, cada temporalidad por separado."

#include <Trade\Trade.mqh>

enum ENUM_VOL_SRC
  {
   VOL_AUTO = 0, // Automático (real si existe, si no ticks)
   VOL_TICK = 1, // Volumen de ticks
   VOL_REAL = 2  // Volumen real
  };

input group "Temporalidades"
input bool   InpUseM1   = true;  // Operar divergencias de M1
input double InpLotsM1  = 0.01;  // Lotes M1
input bool   InpUseM3   = true;  // Operar divergencias de M3
input double InpLotsM3  = 0.01;  // Lotes M3
input bool   InpUseM5   = true;  // Operar divergencias de M5
input double InpLotsM5  = 0.01;  // Lotes M5
input bool   InpUseM15  = true;  // Operar divergencias de M15
input double InpLotsM15 = 0.01;  // Lotes M15

input group "Divergencias (mismos parámetros que el indicador)"
input int          InpPivLen     = 5;        // Longitud de pivote
input ENUM_VOL_SRC InpVolSrc     = VOL_AUTO; // Fuente de volumen
input int          InpWarmupBars = 1500;     // Velas de historia para inicializar

input group "Operativa"
input bool   InpReverse     = true;     // Al cerrar por divergencia contraria, abrir en el nuevo sentido
input bool   InpAllowBuy    = true;     // Permitir compras
input bool   InpAllowSell   = true;     // Permitir ventas
input int    InpMaxSpread   = 0;        // Spread máximo para abrir, en puntos (0 = sin filtro)
input int    InpSlippage    = 30;       // Desvío máximo, en puntos
input ulong  InpMagic       = 2026100;  // Magic base (cada TF usa base + minutos)
input bool   InpShowPanel   = true;     // Mostrar panel en el gráfico
input bool   InpDebug       = false;    // Registrar cada pivote en la pestaña Expertos

//--- estado por temporalidad
struct TFState
  {
   ENUM_TIMEFRAMES   tf;
   string            name;
   bool              enabled;
   double            lots;
   ulong             magic;
   bool              ready;
   datetime          lastBar;     // última vela cerrada procesada
   //--- delta
   double            prevC;
   bool              hasPrevC;
   int               lastSign;
   double            cvdAll;      // CVD continuo (sin reinicios)
   //--- ventana de pivotes (índice 0 = la más vieja)
   double            hi[];
   double            lo[];
   double            cv[];
   //--- última divergencia de referencia
   bool              hasPh;
   double            lastPhP;
   double            lastPhC;
   bool              hasPl;
   double            lastPlP;
   double            lastPlC;
   //--- netting: posición virtual en lotes con signo
   double            vpos;
   string            lastSignal;
   string            lastAction;  // qué hizo el EA con la última señal (o por qué no operó)
   int               liveDivs;    // divergencias detectadas desde que se cargó el EA
  };

TFState g[4];
CTrade  trade;
bool    g_hedging = true;
bool    g_useReal = false;
datetime g_lastTick = 0;
datetime g_started  = 0;

//+------------------------------------------------------------------+
int OnInit()
  {
   if(InpPivLen < 2 || InpPivLen > 20)
     {
      Print("Longitud de pivote fuera de rango (2-20).");
      return INIT_PARAMETERS_INCORRECT;
     }

   ENUM_TIMEFRAMES tfs[4]  = {PERIOD_M1, PERIOD_M3, PERIOD_M5, PERIOD_M15};
   string          nms[4]  = {"M1", "M3", "M5", "M15"};
   bool            use[4]  = {InpUseM1, InpUseM3, InpUseM5, InpUseM15};
   double          lts[4]  = {InpLotsM1, InpLotsM3, InpLotsM5, InpLotsM15};
   int             mins[4] = {1, 3, 5, 15};

   for(int i = 0; i < 4; i++)
     {
      g[i].tf         = tfs[i];
      g[i].name       = nms[i];
      g[i].enabled    = use[i];
      g[i].lots       = lts[i];
      g[i].magic      = InpMagic + mins[i];
      g[i].vpos       = 0.0;
      g[i].lastSignal = "-";
      g[i].lastAction = "-";
      g[i].liveDivs   = 0;
      ResetSignalState(i);
     }

   long mm   = AccountInfoInteger(ACCOUNT_MARGIN_MODE);
   g_hedging = (mm == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING);
   g_useReal = DetectRealVolume();

   trade.SetDeviationInPoints(InpSlippage);
   trade.SetTypeFillingBySymbol(_Symbol);
   trade.SetMarginMode();
   trade.LogLevel(LOG_LEVEL_ERRORS);

   if(!g_hedging)
     {
      LoadVirtual();
      SyncVirtual();
     }

   for(int i = 0; i < 4; i++)
      if(g[i].enabled)
         Warmup(i);

   g_started = TimeCurrent();
   PrintFormat("RIC Div EA iniciado en %s | cuenta %s | volumen %s | lote mín %s, paso %s",
               _Symbol, g_hedging ? "HEDGING" : "NETTING", g_useReal ? "real" : "ticks",
               DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN), VolDigits()),
               DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP), VolDigits()));
   string why = TradeBlockReason();
   if(why != "")
      Print("ATENCIÓN: el EA no va a poder operar: ", why);
   for(int i = 0; i < 4; i++)
      if(g[i].enabled)
         PrintFormat("%s: %s, lote %s, última divergencia en la historia: %s", g[i].name,
                     g[i].ready ? "historia cargada" : "historia todavía no disponible",
                     DoubleToString(NormLots(g[i].lots), VolDigits()), g[i].lastSignal);
   EventSetTimer(5);
   UpdatePanel();
   return INIT_SUCCEEDED;
  }

//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   EventKillTimer();
   Comment("");
  }

// El panel se refresca aunque no lleguen ticks (mercado cerrado)
void OnTimer()
  {
   UpdatePanel();
  }

// Motivo por el que el EA no puede enviar órdenes ("" = puede operar)
string TradeBlockReason()
  {
   if(MQLInfoInteger(MQL_TESTER))
      return "";
   if(!TerminalInfoInteger(TERMINAL_TRADE_ALLOWED))
      return "botón 'Trading algorítmico' apagado en la barra del terminal";
   if(!MQLInfoInteger(MQL_TRADE_ALLOWED))
      return "falta tildar 'Permitir trading algorítmico' en las propiedades del EA (F7 sobre el gráfico)";
   if(!AccountInfoInteger(ACCOUNT_TRADE_ALLOWED))
      return "la cuenta no permite operar (¿sesión con contraseña de inversor?)";
   if(!AccountInfoInteger(ACCOUNT_TRADE_EXPERT))
      return "el broker no permite expertos en esta cuenta";
   if(SymbolInfoInteger(_Symbol, SYMBOL_TRADE_MODE) == SYMBOL_TRADE_MODE_DISABLED)
      return "el símbolo tiene el trading deshabilitado";
   return "";
  }

//+------------------------------------------------------------------+
void OnTick()
  {
   g_lastTick = TimeCurrent();
   bool changed = false;
   for(int i = 0; i < 4; i++)
     {
      if(!g[i].enabled)
         continue;
      if(!g[i].ready)
        {
         if(!Warmup(i))
            continue;
         PrintFormat("%s: historia cargada", g[i].name);
        }

      datetime t1 = iTime(_Symbol, g[i].tf, 1);
      datetime t0 = iTime(_Symbol, g[i].tf, 0);
      if(t1 == 0 || t0 == 0 || t1 <= g[i].lastBar)
         continue;

      MqlRates rr[];
      int n = CopyRates(_Symbol, g[i].tf, g[i].lastBar + 1, t0 - 1, rr);
      if(n <= 0)
         continue;

      for(int k = 0; k < n; k++)
        {
         if(rr[k].time <= g[i].lastBar)
            continue;
         bool bull, bear;
         ProcessBar(i, rr[k], bull, bear);
         g[i].lastBar = rr[k].time;
         // Solo se opera la señal de la última vela cerrada (no señales viejas de una reconexión)
         if(k == n - 1 && (bull || bear))
            OnDivergence(i, bull, bear, rr[k].time);
        }
      changed = true;
     }
   if(changed)
      UpdatePanel();
  }

//+------------------------------------------------------------------+
//| Inicialización con historia (sin operar)                         |
//+------------------------------------------------------------------+
bool Warmup(int i)
  {
   MqlRates rr[];
   int n = CopyRates(_Symbol, g[i].tf, 1, InpWarmupBars, rr);
   if(n < 2 * InpPivLen + 2)
      return false; // historia todavía no disponible; se reintenta en el próximo tick

   ResetSignalState(i);
   for(int k = 0; k < n; k++)
     {
      bool bull, bear;
      ProcessBar(i, rr[k], bull, bear);
      if(bull || bear)
         g[i].lastSignal = (bull ? "ALCISTA " : "BAJISTA ") + TimeToString(rr[k].time - InpPivLen * PeriodSeconds(g[i].tf), TIME_DATE | TIME_MINUTES);
     }
   g[i].lastBar = rr[n - 1].time;
   g[i].ready   = true;
   return true;
  }

//+------------------------------------------------------------------+
void ResetSignalState(int i)
  {
   g[i].ready    = false;
   g[i].lastBar  = 0;
   g[i].prevC    = 0.0;
   g[i].hasPrevC = false;
   g[i].lastSign = 1;
   g[i].cvdAll   = 0.0;
   g[i].hasPh    = false;
   g[i].hasPl    = false;
   g[i].lastPhP  = 0.0;
   g[i].lastPhC  = 0.0;
   g[i].lastPlP  = 0.0;
   g[i].lastPlC  = 0.0;
   ArrayResize(g[i].hi, 0);
   ArrayResize(g[i].lo, 0);
   ArrayResize(g[i].cv, 0);
  }

//+------------------------------------------------------------------+
//| Volumen                                                          |
//+------------------------------------------------------------------+
bool DetectRealVolume()
  {
   if(InpVolSrc == VOL_TICK)
      return false;
   if(InpVolSrc == VOL_REAL)
      return true;
   // Solo se usa el volumen real si casi todas las velas lo traen: si viene en cero en parte
   // de las velas el CVD queda plano y no aparecen divergencias.
   MqlRates r[];
   int n = CopyRates(_Symbol, PERIOD_M1, 1, 200, r);
   if(n <= 0)
      return false;
   int withReal = 0;
   for(int k = 0; k < n; k++)
      if(r[k].real_volume > 0)
         withReal++;
   return withReal >= n * 0.9;
  }

double Vol(const MqlRates &r)
  {
   return g_useReal ? (double)r.real_volume : (double)r.tick_volume;
  }

//+------------------------------------------------------------------+
//| Delta de una vela cerrada (réplica del indicador)                |
//|  M1: estimación por posición del cierre (el indicador en M1 no   |
//|      tiene intrabars). M3/M5/M15: velas M1 internas.             |
//+------------------------------------------------------------------+
double ComputeDelta(int i, const MqlRates &bar)
  {
   int secs = PeriodSeconds(g[i].tf);
   int n = 0;
   MqlRates m1[];
   if(secs > 60)
      n = CopyRates(_Symbol, PERIOD_M1, bar.time, bar.time + secs - 1, m1);

   double delta = 0.0;
   if(n > 1)
     {
      for(int k = 0; k < n; k++)
        {
         double o = m1[k].open;
         double c = m1[k].close;
         double v = Vol(m1[k]);
         int sgn;
         if(c > o)
            sgn = 1;
         else
            if(c < o)
               sgn = -1;
            else
               if(g[i].hasPrevC && c > g[i].prevC)
                  sgn = 1;
               else
                  if(g[i].hasPrevC && c < g[i].prevC)
                     sgn = -1;
                  else
                     sgn = g[i].lastSign;
         delta += sgn * v;
         g[i].prevC    = c;
         g[i].hasPrevC = true;
         g[i].lastSign = sgn;
        }
     }
   else
     {
      double rng = bar.high - bar.low;
      delta = rng > 0 ? Vol(bar) * (2.0 * (bar.close - bar.low) / rng - 1.0) : 0.0;
      g[i].prevC    = bar.close;
      g[i].hasPrevC = true;
     }
   return delta;
  }

//+------------------------------------------------------------------+
//| Procesa una vela cerrada: CVD + pivotes + divergencias           |
//+------------------------------------------------------------------+
void ProcessBar(int i, const MqlRates &bar, bool &bull, bool &bear)
  {
   bull = false;
   bear = false;

   g[i].cvdAll += ComputeDelta(i, bar);

   int s = ArraySize(g[i].hi);
   ArrayResize(g[i].hi, s + 1);
   ArrayResize(g[i].lo, s + 1);
   ArrayResize(g[i].cv, s + 1);
   g[i].hi[s] = bar.high;
   g[i].lo[s] = bar.low;
   g[i].cv[s] = g[i].cvdAll;

   int W = 2 * InpPivLen + 1;
   if(s + 1 > W)
     {
      ArrayRemove(g[i].hi, 0, 1);
      ArrayRemove(g[i].lo, 0, 1);
      ArrayRemove(g[i].cv, 0, 1);
     }
   if(ArraySize(g[i].hi) < W)
      return;

   // Pivote en la vela central: confirmado 'InpPivLen' velas después (no repinta)
   int    c    = InpPivLen;
   double ph   = g[i].hi[c];
   double pl   = g[i].lo[c];
   bool   isPH = true;
   bool   isPL = true;
   for(int k = 0; k < W; k++)
     {
      if(k == c)
         continue;
      if(k < c)
        {
         if(g[i].hi[k] >= ph) isPH = false;
         if(g[i].lo[k] <= pl) isPL = false;
        }
      else
        {
         if(g[i].hi[k] > ph) isPH = false;
         if(g[i].lo[k] < pl) isPL = false;
        }
     }

   double cvdAtPiv = g[i].cv[c];
   if(InpDebug && g[i].ready && (isPH || isPL))
      PrintFormat("%s pivote %s%s precio %s CVD %.0f (anterior máx %s/%.0f, mín %s/%.0f)", g[i].name,
                  isPH ? "MÁX " : "", isPL ? "MÍN " : "", DoubleToString(isPH ? ph : pl, _Digits), cvdAtPiv,
                  DoubleToString(g[i].lastPhP, _Digits), g[i].lastPhC, DoubleToString(g[i].lastPlP, _Digits), g[i].lastPlC);
   if(isPH)
     {
      bear = g[i].hasPh && ph > g[i].lastPhP && cvdAtPiv < g[i].lastPhC;
      g[i].hasPh   = true;
      g[i].lastPhP = ph;
      g[i].lastPhC = cvdAtPiv;
     }
   if(isPL)
     {
      bull = g[i].hasPl && pl < g[i].lastPlP && cvdAtPiv > g[i].lastPlC;
      g[i].hasPl   = true;
      g[i].lastPlP = pl;
      g[i].lastPlC = cvdAtPiv;
     }
  }

//+------------------------------------------------------------------+
//| Gestión de la señal                                              |
//+------------------------------------------------------------------+
void OnDivergence(int i, bool bull, bool bear, datetime barTime)
  {
   string when = TimeToString(barTime - InpPivLen * PeriodSeconds(g[i].tf), TIME_DATE | TIME_MINUTES);
   g[i].lastSignal = (bull && bear ? "DOBLE " : bull ? "ALCISTA " : "BAJISTA ") + when;
   g[i].liveDivs++;
   PrintFormat("%s %s: divergencia %s confirmada (pivote %s)", _Symbol, g[i].name,
               bull && bear ? "alcista y bajista" : bull ? "ALCISTA" : "BAJISTA", when);

   if(!g_hedging)
      SyncVirtual();

   int cur = CurrentDir(i);
   int newDir;
   if(bull && bear)
      newDir = 0; // señales opuestas en la misma vela: se queda afuera
   else
     {
      int sig = bull ? 1 : -1;
      if(cur == sig)
        {
         g[i].lastAction = "ya estaba en ese sentido";
         return;
        }
      newDir = (cur == -sig && !InpReverse) ? 0 : sig;
     }

   if(newDir != 0)
     {
      string no = OpenBlockReason(i, newDir);
      if(no != "")
        {
         PrintFormat("%s: no se abre: %s", g[i].name, no);
         g[i].lastAction = "no abrió: " + no;
         newDir = 0;
        }
     }
   if(newDir == cur)
      return;

   string why = TradeBlockReason();
   if(why != "")
     {
      PrintFormat("%s: señal sin ejecutar: %s", g[i].name, why);
      g[i].lastAction = "sin ejecutar: " + why;
      return;
     }

   if(g_hedging)
      ApplyHedging(i, cur, newDir);
   else
      ApplyNetting(i, newDir);
  }

int CurrentDir(int i)
  {
   if(!g_hedging)
      return g[i].vpos > 1e-9 ? 1 : g[i].vpos < -1e-9 ? -1 : 0;

   int dir = 0;
   for(int k = PositionsTotal() - 1; k >= 0; k--)
     {
      ulong tk = PositionGetTicket(k);
      if(tk == 0 || PositionGetString(POSITION_SYMBOL) != _Symbol || (ulong)PositionGetInteger(POSITION_MAGIC) != g[i].magic)
         continue;
      dir = PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY ? 1 : -1;
     }
   return dir;
  }

// Motivo por el que no se puede abrir en ese sentido ("" = se puede)
string OpenBlockReason(int i, int dir)
  {
   if(dir > 0 && !InpAllowBuy)
      return "compras desactivadas en los parámetros";
   if(dir < 0 && !InpAllowSell)
      return "ventas desactivadas en los parámetros";

   long mode = SymbolInfoInteger(_Symbol, SYMBOL_TRADE_MODE);
   if(dir > 0 && mode != SYMBOL_TRADE_MODE_FULL && mode != SYMBOL_TRADE_MODE_LONGONLY)
      return "el símbolo no admite compras ahora";
   if(dir < 0 && mode != SYMBOL_TRADE_MODE_FULL && mode != SYMBOL_TRADE_MODE_SHORTONLY)
      return "el símbolo no admite ventas ahora";

   if(InpMaxSpread > 0 && SymbolInfoInteger(_Symbol, SYMBOL_SPREAD) > InpMaxSpread)
      return StringFormat("spread %d > %d puntos", (int)SymbolInfoInteger(_Symbol, SYMBOL_SPREAD), InpMaxSpread);

   double lots  = NormLots(g[i].lots);
   double price = dir > 0 ? SymbolInfoDouble(_Symbol, SYMBOL_ASK) : SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double margin;
   if(OrderCalcMargin(dir > 0 ? ORDER_TYPE_BUY : ORDER_TYPE_SELL, _Symbol, lots, price, margin)
      && margin > AccountInfoDouble(ACCOUNT_MARGIN_FREE))
      return StringFormat("margen insuficiente para %s lotes (hace falta %.2f, libre %.2f)",
                          DoubleToString(lots, VolDigits()), margin, AccountInfoDouble(ACCOUNT_MARGIN_FREE));
   return "";
  }

//--- hedging: una posición por TF identificada por su magic
void ApplyHedging(int i, int cur, int newDir)
  {
   trade.SetExpertMagicNumber(g[i].magic);
   if(cur != 0)
     {
      for(int k = PositionsTotal() - 1; k >= 0; k--)
        {
         ulong tk = PositionGetTicket(k);
         if(tk == 0 || PositionGetString(POSITION_SYMBOL) != _Symbol || (ulong)PositionGetInteger(POSITION_MAGIC) != g[i].magic)
            continue;
         if(!trade.PositionClose(tk, InpSlippage))
           {
            PrintFormat("%s: no se pudo cerrar #%I64u (%d %s)", g[i].name, tk, trade.ResultRetcode(), trade.ResultRetcodeDescription());
            g[i].lastAction = "error al cerrar: " + trade.ResultRetcodeDescription();
            return;
           }
         g[i].lastAction = "cerró";
        }
     }
   if(newDir != 0)
     {
      double lots = NormLots(g[i].lots);
      string cmt  = "RIC Div " + g[i].name;
      bool ok = newDir > 0 ? trade.Buy(lots, _Symbol, 0, 0, 0, cmt) : trade.Sell(lots, _Symbol, 0, 0, 0, cmt);
      if(!ok || !RetcodeOk(trade.ResultRetcode()))
        {
         PrintFormat("%s: no se pudo abrir (%d %s)", g[i].name, trade.ResultRetcode(), trade.ResultRetcodeDescription());
         g[i].lastAction = "error al abrir: " + trade.ResultRetcodeDescription();
        }
      else
         g[i].lastAction = newDir > 0 ? "abrió COMPRA" : "abrió VENTA";
     }
  }

//--- netting: se ajusta la posición neta por la diferencia de la TF
void ApplyNetting(int i, int newDir)
  {
   double target = newDir * NormLots(g[i].lots);
   double diff   = NormalizeDouble(target - g[i].vpos, VolDigits());
   if(MathAbs(diff) < 1e-9)
      return;

   trade.SetExpertMagicNumber(InpMagic);
   string cmt  = "RIC Div " + g[i].name;
   double vmax = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double rest = MathAbs(diff);
   double done = 0.0;
   while(rest > 1e-9)
     {
      double v = NormalizeDouble(vmax > 0 ? MathMin(rest, vmax) : rest, VolDigits());
      bool ok = diff > 0 ? trade.Buy(v, _Symbol, 0, 0, 0, cmt) : trade.Sell(v, _Symbol, 0, 0, 0, cmt);
      if(!ok || !RetcodeOk(trade.ResultRetcode()))
        {
         PrintFormat("%s: orden de %.2f lotes rechazada (%d %s)", g[i].name, v, trade.ResultRetcode(), trade.ResultRetcodeDescription());
         g[i].lastAction = "orden rechazada: " + trade.ResultRetcodeDescription();
         break;
        }
      done += v;
      rest -= v;
     }
   g[i].vpos = NormalizeDouble(g[i].vpos + (diff > 0 ? done : -done), VolDigits());
   SaveVirtual(i);
   if(rest <= 1e-9)
      g[i].lastAction = newDir > 0 ? "posición virtual COMPRADA" : newDir < 0 ? "posición virtual VENDIDA" : "cerró";
  }

bool RetcodeOk(uint rc)
  {
   return rc == TRADE_RETCODE_DONE || rc == TRADE_RETCODE_DONE_PARTIAL || rc == TRADE_RETCODE_PLACED;
  }

//--- persistencia de las posiciones virtuales (netting)
string GVName(int i)
  {
   return StringFormat("RICDiv_%s_%I64u_%s", _Symbol, InpMagic, g[i].name);
  }

void LoadVirtual()
  {
   if(MQLInfoInteger(MQL_TESTER))
      return;
   for(int i = 0; i < 4; i++)
      if(GlobalVariableCheck(GVName(i)))
         g[i].vpos = GlobalVariableGet(GVName(i));
  }

void SaveVirtual(int i)
  {
   if(!MQLInfoInteger(MQL_TESTER))
      GlobalVariableSet(GVName(i), g[i].vpos);
  }

// Si la posición del símbolo se cerró por fuera del EA (manual, stop out), se ponen en cero las virtuales
void SyncVirtual()
  {
   double expected = 0.0;
   for(int i = 0; i < 4; i++)
      expected += g[i].vpos;
   if(MathAbs(expected) > 1e-9 && !PositionSelect(_Symbol))
     {
      Print("La posición neta ya no existe: se reinician las posiciones virtuales.");
      for(int i = 0; i < 4; i++)
        {
         g[i].vpos = 0.0;
         SaveVirtual(i);
        }
     }
  }

//+------------------------------------------------------------------+
//| Lotes válidos para cualquier símbolo                             |
//+------------------------------------------------------------------+
int VolDigits()
  {
   double step = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   int d = 0;
   while(d < 8 && MathAbs(step * MathPow(10, d) - MathRound(step * MathPow(10, d))) > 1e-7)
      d++;
   return d;
  }

double NormLots(double lots)
  {
   double vmin = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double vmax = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double step = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   if(step <= 0)
      step = vmin > 0 ? vmin : 0.01;
   double v = MathFloor(lots / step + 1e-7) * step;
   if(v < vmin)
      v = vmin;
   if(g_hedging && vmax > 0 && v > vmax)
      v = vmax;
   return NormalizeDouble(v, VolDigits());
  }

//+------------------------------------------------------------------+
void UpdatePanel()
  {
   if(!InpShowPanel || (MQLInfoInteger(MQL_TESTER) && !MQLInfoInteger(MQL_VISUAL_MODE)))
      return;
   string txt = StringFormat("RIC Delta Divergencias EA · %s · %s · vol %s\n",
                             _Symbol, g_hedging ? "hedging" : "netting", g_useReal ? "real" : "ticks");
   string why = TradeBlockReason();
   txt += why == "" ? "Trading: habilitado\n" : "TRADING BLOQUEADO: " + why + "\n";
   txt += g_lastTick == 0 ? "Sin ticks desde que se cargó el EA (¿mercado cerrado?)\n"
                          : "Último tick: " + TimeToString(g_lastTick, TIME_DATE | TIME_SECONDS) + "\n";
   for(int i = 0; i < 4; i++)
     {
      if(!g[i].enabled)
        {
         txt += g[i].name + ": desactivada\n";
         continue;
        }
      int d = CurrentDir(i);
      txt += StringFormat("%s: %s | última div: %s | en vivo: %d | acción: %s%s\n", g[i].name,
                          d > 0 ? "COMPRADO" : d < 0 ? "VENDIDO" : "sin posición",
                          g[i].lastSignal, g[i].liveDivs, g[i].lastAction,
                          g[i].ready ? "" : " (cargando historia)");
     }
   Comment(txt);
  }
//+------------------------------------------------------------------+

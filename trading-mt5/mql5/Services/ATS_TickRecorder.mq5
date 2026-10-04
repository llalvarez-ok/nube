//+------------------------------------------------------------------+
//| ATS_TickRecorder.mq5                                             |
//| Servicio de MT5: graba todos los ticks recibidos, el ping y las  |
//| especificaciones de cada símbolo. No opera: solo observa.        |
//|                                                                  |
//| Salida (carpeta común de los terminales: ...\Common\Files\ATS\): |
//|   ticks\<SIMBOLO>\<AAAAMMDD>.bin  registros de 52 bytes (ver doc)|
//|   status\<AAAAMMDD>.csv           ping, conexión y spread         |
//|   specs\<SIMBOLO>_<AAAAMMDD>.csv  especificaciones del símbolo    |
//|   events.csv                      inicio, fin y errores           |
//+------------------------------------------------------------------+
#property service
#property version     "1.00"
#property description "ATS Tick Recorder: graba ticks, spread, ping y especificaciones. No opera."

input string InpSymbols        = "XAUUSDc"; // Símbolos separados por coma
input int    InpPollMs         = 10;        // Intervalo de consulta de ticks (ms)
input int    InpStatusEverySec = 10;        // Cada cuántos segundos registrar ping y estado
input string InpRootFolder     = "ATS";     // Carpeta dentro de Common\Files

#define MAX_TICKS_PER_POLL 100000

//+------------------------------------------------------------------+
//| Utilidades                                                       |
//+------------------------------------------------------------------+
string DayKeyFromMsc(const long msc)
  {
   MqlDateTime dt;
   TimeToStruct((datetime)(msc / 1000), dt);
   return StringFormat("%04d%02d%02d", dt.year, dt.mon, dt.day);
  }

string DayKeyFromTime(const datetime t)
  {
   MqlDateTime dt;
   TimeToStruct(t, dt);
   return StringFormat("%04d%02d%02d", dt.year, dt.mon, dt.day);
  }

void EnsureFolder(const string folder)
  {
   // FolderCreate devuelve false si la carpeta ya existe; no es un error.
   FolderCreate(folder, FILE_COMMON);
  }

// Agrega una línea a un archivo de texto de la carpeta común.
bool AppendLine(const string path, const string line, const string header = "")
  {
   int h = FileOpen(path, FILE_READ | FILE_WRITE | FILE_TXT | FILE_ANSI | FILE_COMMON | FILE_SHARE_READ);
   if(h == INVALID_HANDLE)
     {
      PrintFormat("ATS_TickRecorder: no se pudo abrir %s (error %d)", path, GetLastError());
      return false;
     }
   if(FileSize(h) == 0 && header != "")
      FileWriteString(h, header + "\n");
   FileSeek(h, 0, SEEK_END);
   FileWriteString(h, line + "\n");
   FileClose(h);
   return true;
  }

void LogEvent(const string type, const string detail)
  {
   string line = StringFormat("%s;%s;%s;%s",
                              TimeToString(TimeGMT(), TIME_DATE | TIME_SECONDS),
                              IntegerToString((long)GetMicrosecondCount()),
                              type, detail);
   AppendLine(InpRootFolder + "\\events.csv", line, "gmt_time;mono_us;type;detail");
   Print("ATS_TickRecorder: ", type, " ", detail);
  }

//+------------------------------------------------------------------+
//| Especificaciones del símbolo y de la cuenta                      |
//+------------------------------------------------------------------+
void WriteSpecs(const string symbol, const string day)
  {
   string folder = InpRootFolder + "\\specs";
   EnsureFolder(folder);
   string path = folder + "\\" + symbol + "_" + day + ".csv";
   int h = FileOpen(path, FILE_WRITE | FILE_TXT | FILE_ANSI | FILE_COMMON);
   if(h == INVALID_HANDLE)
     {
      LogEvent("ERROR", StringFormat("specs %s error %d", symbol, GetLastError()));
      return;
     }
   FileWriteString(h, "key;value\n");
   FileWriteString(h, "written_gmt;" + TimeToString(TimeGMT(), TIME_DATE | TIME_SECONDS) + "\n");
   FileWriteString(h, "symbol;" + symbol + "\n");
   FileWriteString(h, "description;" + SymbolInfoString(symbol, SYMBOL_DESCRIPTION) + "\n");
   FileWriteString(h, "path;" + SymbolInfoString(symbol, SYMBOL_PATH) + "\n");
   FileWriteString(h, "currency_base;" + SymbolInfoString(symbol, SYMBOL_CURRENCY_BASE) + "\n");
   FileWriteString(h, "currency_profit;" + SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT) + "\n");
   FileWriteString(h, "currency_margin;" + SymbolInfoString(symbol, SYMBOL_CURRENCY_MARGIN) + "\n");
   FileWriteString(h, "digits;" + IntegerToString(SymbolInfoInteger(symbol, SYMBOL_DIGITS)) + "\n");
   FileWriteString(h, "point;" + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_POINT), 10) + "\n");
   FileWriteString(h, "tick_size;" + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE), 10) + "\n");
   FileWriteString(h, "tick_value;" + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE), 10) + "\n");
   FileWriteString(h, "contract_size;" + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE), 4) + "\n");
   FileWriteString(h, "volume_min;" + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN), 4) + "\n");
   FileWriteString(h, "volume_max;" + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX), 4) + "\n");
   FileWriteString(h, "volume_step;" + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP), 4) + "\n");
   FileWriteString(h, "volume_limit;" + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_VOLUME_LIMIT), 4) + "\n");
   FileWriteString(h, "spread_points_now;" + IntegerToString(SymbolInfoInteger(symbol, SYMBOL_SPREAD)) + "\n");
   FileWriteString(h, "spread_float;" + IntegerToString(SymbolInfoInteger(symbol, SYMBOL_SPREAD_FLOAT)) + "\n");
   FileWriteString(h, "stops_level;" + IntegerToString(SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL)) + "\n");
   FileWriteString(h, "freeze_level;" + IntegerToString(SymbolInfoInteger(symbol, SYMBOL_TRADE_FREEZE_LEVEL)) + "\n");
   FileWriteString(h, "trade_mode;" + IntegerToString(SymbolInfoInteger(symbol, SYMBOL_TRADE_MODE)) + "\n");
   FileWriteString(h, "trade_exemode;" + IntegerToString(SymbolInfoInteger(symbol, SYMBOL_TRADE_EXEMODE)) + "\n");
   FileWriteString(h, "filling_mode;" + IntegerToString(SymbolInfoInteger(symbol, SYMBOL_FILLING_MODE)) + "\n");
   FileWriteString(h, "order_mode;" + IntegerToString(SymbolInfoInteger(symbol, SYMBOL_ORDER_MODE)) + "\n");
   FileWriteString(h, "calc_mode;" + IntegerToString(SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE)) + "\n");
   FileWriteString(h, "swap_long;" + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_SWAP_LONG), 4) + "\n");
   FileWriteString(h, "swap_short;" + DoubleToString(SymbolInfoDouble(symbol, SYMBOL_SWAP_SHORT), 4) + "\n");
   // Datos de cuenta sin identificar al titular (sin número de cuenta ni nombre).
   FileWriteString(h, "account_company;" + AccountInfoString(ACCOUNT_COMPANY) + "\n");
   FileWriteString(h, "account_server;" + AccountInfoString(ACCOUNT_SERVER) + "\n");
   FileWriteString(h, "account_currency;" + AccountInfoString(ACCOUNT_CURRENCY) + "\n");
   FileWriteString(h, "account_leverage;" + IntegerToString(AccountInfoInteger(ACCOUNT_LEVERAGE)) + "\n");
   FileWriteString(h, "account_trade_mode;" + IntegerToString(AccountInfoInteger(ACCOUNT_TRADE_MODE)) + "\n");
   FileWriteString(h, "account_margin_mode;" + IntegerToString(AccountInfoInteger(ACCOUNT_MARGIN_MODE)) + "\n");
   FileWriteString(h, "account_limit_orders;" + IntegerToString(AccountInfoInteger(ACCOUNT_LIMIT_ORDERS)) + "\n");
   FileWriteString(h, "terminal_build;" + IntegerToString(TerminalInfoInteger(TERMINAL_BUILD)) + "\n");
   FileClose(h);
  }

//+------------------------------------------------------------------+
//| Grabador de un símbolo                                           |
//+------------------------------------------------------------------+
class CSymbolRecorder
  {
private:
   string            m_symbol;
   long              m_last_msc;      // time_msc del último tick escrito
   int               m_dup;           // ticks ya escritos con time_msc == m_last_msc
   int               m_handle;
   string            m_day;
   long              m_written_total;
   long              m_errors;

   bool              OpenDay(const string day)
     {
      CloseFile();
      string folder = InpRootFolder + "\\ticks\\" + m_symbol;
      EnsureFolder(InpRootFolder);
      EnsureFolder(InpRootFolder + "\\ticks");
      EnsureFolder(folder);
      string path = folder + "\\" + day + ".bin";
      // READ|WRITE no trunca: si el servicio se reinicia, se agrega al final.
      m_handle = FileOpen(path, FILE_READ | FILE_WRITE | FILE_BIN | FILE_COMMON | FILE_SHARE_READ);
      if(m_handle == INVALID_HANDLE)
        {
         m_errors++;
         LogEvent("ERROR", StringFormat("no se pudo abrir %s (error %d)", path, GetLastError()));
         return false;
        }
      FileSeek(m_handle, 0, SEEK_END);
      m_day = day;
      return true;
     }

   void              WriteTick(const MqlTick &t, const ulong local_us)
     {
      if(m_handle == INVALID_HANDLE)
         return;
      // Registro de 52 bytes, little-endian. El orden no se cambia sin cambiar
      // también research/ticks/formato.py.
      FileWriteLong(m_handle, t.time_msc);                // 8: hora del servidor en ms
      FileWriteDouble(m_handle, t.bid);                   // 8
      FileWriteDouble(m_handle, t.ask);                   // 8
      FileWriteDouble(m_handle, t.last);                  // 8
      FileWriteDouble(m_handle, t.volume_real);           // 8
      FileWriteInteger(m_handle, (int)t.flags, INT_VALUE);// 4
      FileWriteLong(m_handle, (long)local_us);            // 8: reloj monotónico local al leerlo
      m_written_total++;
     }

public:
                     CSymbolRecorder(void) : m_symbol(""), m_last_msc(0), m_dup(0),
                     m_handle(INVALID_HANDLE), m_day(""), m_written_total(0), m_errors(0) {}
                    ~CSymbolRecorder(void) { CloseFile(); }

   string            Name(void) const { return m_symbol; }
   long              WrittenTotal(void) const { return m_written_total; }
   long              Errors(void) const { return m_errors; }

   bool              Init(const string symbol)
     {
      m_symbol = symbol;
      if(!SymbolSelect(symbol, true))
        {
         LogEvent("ERROR", StringFormat("símbolo %s no disponible (error %d)", symbol, GetLastError()));
         return false;
        }
      MqlTick t;
      if(SymbolInfoTick(symbol, t) && t.time_msc > 0)
         m_last_msc = t.time_msc + 1;
      else
         m_last_msc = (long)TimeTradeServer() * 1000;
      m_dup = 0;
      LogEvent("START_SYMBOL", StringFormat("%s desde time_msc=%s", symbol, IntegerToString(m_last_msc)));
      return true;
     }

   // Lee los ticks nuevos y los escribe. Devuelve la cantidad escrita.
   int               Poll(void)
     {
      MqlTick ticks[];
      int n = CopyTicks(m_symbol, ticks, COPY_TICKS_ALL, (ulong)m_last_msc, MAX_TICKS_PER_POLL);
      if(n <= 0)
        {
         if(n < 0)
            m_errors++;
         return 0;
        }
      ulong local_us = GetMicrosecondCount();

      // CopyTicks devuelve también los ticks del milisegundo m_last_msc que ya
      // escribimos en la consulta anterior: se saltean.
      int start = 0;
      while(start < n && start < m_dup && ticks[start].time_msc == m_last_msc)
         start++;

      int written = 0;
      for(int i = start; i < n; i++)
        {
         string day = DayKeyFromMsc(ticks[i].time_msc);
         if(day != m_day || m_handle == INVALID_HANDLE)
            OpenDay(day);
         WriteTick(ticks[i], local_us);
         written++;
        }

      long new_last = ticks[n - 1].time_msc;
      int same = 0;
      for(int i = n - 1; i >= 0 && ticks[i].time_msc == new_last; i--)
         same++;
      m_last_msc = new_last;
      m_dup = same;
      return written;
     }

   void              Flush(void)
     {
      if(m_handle != INVALID_HANDLE)
         FileFlush(m_handle);
     }

   void              CloseFile(void)
     {
      if(m_handle != INVALID_HANDLE)
        {
         FileClose(m_handle);
         m_handle = INVALID_HANDLE;
        }
     }
  };

//+------------------------------------------------------------------+
//| Estado: ping, conexión y spread actual                           |
//+------------------------------------------------------------------+
void WriteStatus(CSymbolRecorder &recs[])
  {
   string folder = InpRootFolder + "\\status";
   EnsureFolder(folder);
   string path = folder + "\\" + DayKeyFromTime(TimeGMT()) + ".csv";
   string header = "mono_us;server_time;gmt_time;local_time;connected;ping_us;symbol;bid;ask;spread_points;ticks_written;errors";

   string mono    = IntegerToString((long)GetMicrosecondCount());
   string server  = TimeToString(TimeTradeServer(), TIME_DATE | TIME_SECONDS);
   string gmt     = TimeToString(TimeGMT(), TIME_DATE | TIME_SECONDS);
   string local   = TimeToString(TimeLocal(), TIME_DATE | TIME_SECONDS);
   string conn    = IntegerToString(TerminalInfoInteger(TERMINAL_CONNECTED));
   string ping    = IntegerToString(TerminalInfoInteger(TERMINAL_PING_LAST));

   for(int i = 0; i < ArraySize(recs); i++)
     {
      string sym = recs[i].Name();
      MqlTick t;
      double bid = 0.0, ask = 0.0, spread = 0.0;
      if(SymbolInfoTick(sym, t))
        {
         bid = t.bid;
         ask = t.ask;
         double point = SymbolInfoDouble(sym, SYMBOL_POINT);
         if(point > 0.0)
            spread = (ask - bid) / point;
        }
      int digits = (int)SymbolInfoInteger(sym, SYMBOL_DIGITS);
      string line = StringFormat("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s",
                                 mono, server, gmt, local, conn, ping, sym,
                                 DoubleToString(bid, digits), DoubleToString(ask, digits),
                                 DoubleToString(spread, 1),
                                 IntegerToString(recs[i].WrittenTotal()),
                                 IntegerToString(recs[i].Errors()));
      AppendLine(path, line, header);
     }
  }

//+------------------------------------------------------------------+
//| Programa principal del servicio                                  |
//+------------------------------------------------------------------+
void OnStart()
  {
   EnsureFolder(InpRootFolder);

   string parts[];
   int k = StringSplit(InpSymbols, ',', parts);
   CSymbolRecorder recs[];
   int count = 0;
   for(int i = 0; i < k; i++)
     {
      string sym = parts[i];
      StringTrimLeft(sym);
      StringTrimRight(sym);
      if(sym == "")
         continue;
      ArrayResize(recs, count + 1);
      if(recs[count].Init(sym))
         count++;
      else
         ArrayResize(recs, count);
     }
   if(count == 0)
     {
      LogEvent("STOP", "no hay símbolos válidos en InpSymbols=" + InpSymbols);
      return;
     }

   LogEvent("START", StringFormat("símbolos=%s poll_ms=%d gmt=%s local=%s",
                                  InpSymbols, InpPollMs,
                                  TimeToString(TimeGMT(), TIME_DATE | TIME_SECONDS),
                                  TimeToString(TimeLocal(), TIME_DATE | TIME_SECONDS)));

   string spec_day = DayKeyFromTime(TimeTradeServer());
   for(int i = 0; i < count; i++)
      WriteSpecs(recs[i].Name(), spec_day);

   ulong last_flush  = GetMicrosecondCount();
   ulong last_status = 0;
   ulong status_us   = (ulong)MathMax(1, InpStatusEverySec) * 1000000;

   while(!IsStopped())
     {
      for(int i = 0; i < count; i++)
         recs[i].Poll();

      ulong now = GetMicrosecondCount();
      if(now - last_flush >= 1000000)
        {
         for(int i = 0; i < count; i++)
            recs[i].Flush();
         last_flush = now;
        }
      if(last_status == 0 || now - last_status >= status_us)
        {
         WriteStatus(recs);
         last_status = now;
         string day = DayKeyFromTime(TimeTradeServer());
         if(day != spec_day)
           {
            spec_day = day;
            for(int i = 0; i < count; i++)
               WriteSpecs(recs[i].Name(), spec_day);
           }
        }
      Sleep(MathMax(1, InpPollMs));
     }

   for(int i = 0; i < count; i++)
      recs[i].CloseFile();
   LogEvent("STOP", "servicio detenido");
  }
//+------------------------------------------------------------------+

import * as SQLite from 'expo-sqlite';

let db: SQLite.SQLiteDatabase | null = null;

export async function getDb(): Promise<SQLite.SQLiteDatabase> {
  if (!db) {
    db = await SQLite.openDatabaseAsync('golden_hour.db');
    await initSchema(db);
  }
  return db;
}

async function initSchema(db: SQLite.SQLiteDatabase): Promise<void> {
  await db.execAsync(`
    PRAGMA journal_mode = WAL;

    CREATE TABLE IF NOT EXISTS patients (
      id TEXT PRIMARY KEY,
      facility_id TEXT NOT NULL,
      age REAL NOT NULL,
      sex TEXT NOT NULL,
      pregnancy_status INTEGER DEFAULT 0,
      gestational_weeks INTEGER,
      created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS assessments (
      id TEXT PRIMARY KEY,
      patient_id TEXT NOT NULL,
      facility_id TEXT NOT NULL,
      vitals TEXT NOT NULL,
      news2_score INTEGER NOT NULL,
      risk_band TEXT NOT NULL,
      condition_detected TEXT NOT NULL,
      action_card_id TEXT,
      gps_lat REAL,
      gps_lon REAL,
      created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS sync_queue (
      id TEXT PRIMARY KEY,
      table_name TEXT NOT NULL,
      record_data TEXT NOT NULL,
      client_id TEXT NOT NULL,
      created_at TEXT NOT NULL,
      attempts INTEGER DEFAULT 0,
      last_error TEXT,
      status TEXT DEFAULT 'PENDING'
    );

    CREATE TABLE IF NOT EXISTS settings (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_sync_queue_status ON sync_queue(status);
    CREATE INDEX IF NOT EXISTS idx_assessments_created ON assessments(created_at DESC);
  `);
}

export async function getSetting(key: string): Promise<string | null> {
  const db = await getDb();
  const row = await db.getFirstAsync<{ value: string }>('SELECT value FROM settings WHERE key = ?', [key]);
  return row?.value ?? null;
}

export async function setSetting(key: string, value: string): Promise<void> {
  const db = await getDb();
  await db.runAsync('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', [key, value]);
}

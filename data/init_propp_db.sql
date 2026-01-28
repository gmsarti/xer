-- SQLite Schema for Multilingual Folktales

PRAGMA foreign_keys = ON;

-- Core tales metadata
CREATE TABLE IF NOT EXISTS tales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    author TEXT,
    source TEXT,
    region TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Multilingual content for tales
CREATE TABLE IF NOT EXISTS tale_translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tale_id INTEGER NOT NULL,
    language_code TEXT NOT NULL, -- 'en', 'pt-br', 'es'
    title TEXT,
    story_body TEXT,
    moral TEXT,
    word_count INTEGER,
    reading_time REAL,
    flesch_reading_ease REAL,
    dale_chall_readability REAL,
    FOREIGN KEY (tale_id) REFERENCES tales(id) ON DELETE CASCADE,
    UNIQUE(tale_id, language_code)
);

-- Tags (shared across languages)
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

-- Multilingual names for tags
CREATE TABLE IF NOT EXISTS tag_translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id INTEGER NOT NULL,
    language_code TEXT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    UNIQUE(tag_id, language_code)
);

-- Relationship between tales and tags
CREATE TABLE IF NOT EXISTS tale_tags (
    tale_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (tale_id, tag_id),
    FOREIGN KEY (tale_id) REFERENCES tales(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Entities (shared across languages)
CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tale_id INTEGER NOT NULL,
    type TEXT,
    FOREIGN KEY (tale_id) REFERENCES tales(id) ON DELETE CASCADE
);

-- Multilingual names for entities
CREATE TABLE IF NOT EXISTS entity_translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,
    language_code TEXT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (entity_id) REFERENCES entities(id) ON DELETE CASCADE,
    UNIQUE(entity_id, language_code)
);

-- AI/Analysis metadata
CREATE TABLE IF NOT EXISTS analysis_metadata (
    tale_id INTEGER PRIMARY KEY,
    image_prompt TEXT,
    voice_profile TEXT,
    mood TEXT,
    FOREIGN KEY (tale_id) REFERENCES tales(id) ON DELETE CASCADE
);

-- Christopher Booker's analysis
CREATE TABLE IF NOT EXISTS booker_analysis (
    tale_id INTEGER PRIMARY KEY,
    archetype TEXT,
    confidence REAL,
    analysis TEXT,
    FOREIGN KEY (tale_id) REFERENCES tales(id) ON DELETE CASCADE
);

-- Vladimir Propp's analysis
CREATE TABLE IF NOT EXISTS propp_analysis (
    tale_id INTEGER PRIMARY KEY,
    functions TEXT, -- JSON string
    sequence TEXT,
    type TEXT,
    notes TEXT,
    characters_list TEXT, -- JSON string
    characters_roles TEXT, -- JSON string
    characters_justification TEXT, -- JSON string
    FOREIGN KEY (tale_id) REFERENCES tales(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tale_translations_lang ON tale_translations(language_code);
CREATE INDEX IF NOT EXISTS idx_tag_translations_name ON tag_translations(name);
CREATE INDEX IF NOT EXISTS idx_entity_translations_name ON entity_translations(name);

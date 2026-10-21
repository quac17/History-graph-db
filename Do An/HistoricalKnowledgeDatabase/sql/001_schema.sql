-- PostgreSQL là master registry: cấp mã mờ, giữ danh xưng, nguồn và log.
-- Mã không chứa tên hay năm. Ba bảng ref_* là danh mục, không cấp entity_id.

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE SEQUENCE IF NOT EXISTS seq_person START 1;
CREATE SEQUENCE IF NOT EXISTS seq_event START 1;
CREATE SEQUENCE IF NOT EXISTS seq_group START 1;
CREATE SEQUENCE IF NOT EXISTS seq_place START 1;
CREATE SEQUENCE IF NOT EXISTS seq_time START 1;
CREATE SEQUENCE IF NOT EXISTS seq_artifact START 1;
CREATE SEQUENCE IF NOT EXISTS seq_concept START 1;
CREATE SEQUENCE IF NOT EXISTS seq_source START 1;

CREATE TABLE IF NOT EXISTS ref_historical_eras (
    era_id VARCHAR(20) PRIMARY KEY,
    dynasty_name VARCHAR(100) NOT NULL,
    king_name VARCHAR(100),
    era_name VARCHAR(100) NOT NULL,
    start_year_solar INT,
    end_year_solar INT
);

CREATE TABLE IF NOT EXISTS ref_ganzhi_cycles (
    ganzhi_name VARCHAR(50) PRIMARY KEY,
    stem_vi VARCHAR(20) NOT NULL,
    branch_vi VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS ref_measurement_units (
    unit_id VARCHAR(30) PRIMARY KEY,
    raw_unit_name VARCHAR(50) NOT NULL,
    category VARCHAR(30) NOT NULL,
    si_unit VARCHAR(20),
    conversion_factor NUMERIC(12, 4),
    historical_context VARCHAR(255) NOT NULL
);

-- dim_entities là bản ghi chung và điểm neo của mã. Thuộc tính riêng nằm ở entity_*.
CREATE TABLE IF NOT EXISTS dim_entities (
    entity_id VARCHAR(20) PRIMARY KEY,
    entity_type VARCHAR(20) NOT NULL CHECK (entity_type IN (
        'Person', 'Group', 'Event', 'Place', 'TimeSpan', 'Artifact', 'Concept', 'Source'
    )),
    canonical_name VARCHAR(255) NOT NULL,
    wikidata_id VARCHAR(32),
    verification_status VARCHAR(20) NOT NULL DEFAULT 'DRAFT' CHECK (
        verification_status IN ('DRAFT', 'VERIFIED', 'FLAGGED')
    ),
    confidence_score NUMERIC(4, 3),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS entity_persons (
    entity_id VARCHAR(20) PRIMARY KEY REFERENCES dim_entities (entity_id) ON DELETE CASCADE,
    historical_role_class VARCHAR(40) CHECK (
        historical_role_class IS NULL OR historical_role_class IN (
            'Monarch', 'MilitaryCommander', 'ScholarOfficial', 'ReligiousFigure',
            'CulturalCreator', 'CivilianWitness', 'Diplomat'
        )
    ),
    birth_year INT,
    death_year INT
);

CREATE TABLE IF NOT EXISTS entity_groups (
    entity_id VARCHAR(20) PRIMARY KEY REFERENCES dim_entities (entity_id) ON DELETE CASCADE,
    group_type VARCHAR(40) CHECK (
        group_type IS NULL OR group_type IN (
            'Dynasty', 'ImperialCourt', 'MilitaryForce', 'SocialClass',
            'ReligiousSect', 'InternationalOrg', 'RebelFaction'
        )
    )
);

CREATE TABLE IF NOT EXISTS entity_events (
    entity_id VARCHAR(20) PRIMARY KEY REFERENCES dim_entities (entity_id) ON DELETE CASCADE,
    event_type VARCHAR(40) CHECK (
        event_type IS NULL OR event_type IN (
            'MilitaryBattle', 'PoliticalReform', 'Diplomacy', 'CulturalReligious',
            'UprisingRebellion', 'PersonalMilestone', 'SocioEconomicEvent'
        )
    )
);

CREATE TABLE IF NOT EXISTS entity_places (
    entity_id VARCHAR(20) PRIMARY KEY REFERENCES dim_entities (entity_id) ON DELETE CASCADE,
    spatial_category VARCHAR(40) CHECK (
        spatial_category IS NULL OR spatial_category IN (
            'AdministrativeCenter', 'Battlefield', 'StrategicPass', 'WaterwayPort',
            'CulturalSite', 'NaturalLandmark'
        )
    ),
    modern_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS entity_timespans (
    entity_id VARCHAR(20) PRIMARY KEY REFERENCES dim_entities (entity_id) ON DELETE CASCADE,
    temporal_granularity VARCHAR(20) CHECK (
        temporal_granularity IS NULL OR temporal_granularity IN (
            'ExactDay', 'MonthYear', 'SpecificYear', 'RegnalEra', 'DynasticPeriod', 'Century'
        )
    ),
    raw_text VARCHAR(255),
    lunar_day INT,
    lunar_month INT,
    lunar_year_ganzhi VARCHAR(50) REFERENCES ref_ganzhi_cycles (ganzhi_name),
    era_id VARCHAR(20) REFERENCES ref_historical_eras (era_id),
    era_year INT,
    solar_year_start INT,
    solar_year_end INT,
    solar_date_iso_start DATE,
    solar_date_iso_end DATE
);

CREATE TABLE IF NOT EXISTS entity_artifacts (
    entity_id VARCHAR(20) PRIMARY KEY REFERENCES dim_entities (entity_id) ON DELETE CASCADE,
    artifact_type VARCHAR(40) CHECK (
        artifact_type IS NULL OR artifact_type IN (
            'WeaponEquipment', 'LiteraryWork', 'Epigraphy', 'MonumentArchitecture',
            'SacredRelic', 'HistoricalDocument'
        )
    )
);

CREATE TABLE IF NOT EXISTS entity_concepts (
    entity_id VARCHAR(20) PRIMARY KEY REFERENCES dim_entities (entity_id) ON DELETE CASCADE,
    concept_category VARCHAR(40) CHECK (
        concept_category IS NULL OR concept_category IN (
            'MilitaryTactic', 'GrandStrategy', 'GovernancePhilosophy',
            'IdeologicalDoctrine', 'DiplomaticPrinciple'
        )
    )
);

CREATE TABLE IF NOT EXISTS entity_sources (
    entity_id VARCHAR(20) PRIMARY KEY REFERENCES dim_entities (entity_id) ON DELETE CASCADE,
    source_perspective VARCHAR(40) CHECK (
        source_perspective IS NULL OR source_perspective IN (
            'DomesticOfficial', 'ForeignHostile', 'PrivateScholarly',
            'Archaeological', 'FolkTradition'
        )
    )
);

CREATE TABLE IF NOT EXISTS entity_aliases (
    alias_id BIGSERIAL PRIMARY KEY,
    entity_id VARCHAR(20) NOT NULL REFERENCES dim_entities (entity_id),
    alias_name VARCHAR(255) NOT NULL,
    alias_type VARCHAR(40) NOT NULL,
    source_citation TEXT,
    UNIQUE (entity_id, alias_name)
);

CREATE INDEX IF NOT EXISTS entity_aliases_name_trgm
    ON entity_aliases USING gin (alias_name gin_trgm_ops);

CREATE TABLE IF NOT EXISTS source_documents (
    source_id VARCHAR(20) PRIMARY KEY REFERENCES dim_entities (entity_id),
    title VARCHAR(255) NOT NULL,
    author_compiler VARCHAR(255),
    compilation_era VARCHAR(100),
    source_perspective VARCHAR(40),
    storage_path TEXT,
    doc_status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (doc_status IN ('ACTIVE', 'SUPERSEDED')),
    doc_version VARCHAR(20) NOT NULL DEFAULT '1'
);

CREATE TABLE IF NOT EXISTS raw_documents (
    doc_id VARCHAR(40) PRIMARY KEY,
    source_id VARCHAR(20) NOT NULL REFERENCES source_documents (source_id),
    text TEXT NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    chunk_status VARCHAR(20) CHECK (chunk_status IS NULL OR chunk_status = 'REJECTED')
);

CREATE TABLE IF NOT EXISTS extraction_runs (
    run_id BIGSERIAL PRIMARY KEY,
    doc_id VARCHAR(40) REFERENCES raw_documents (doc_id),
    model_name VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    json_path TEXT
);

CREATE TABLE IF NOT EXISTS ingest_logs (
    log_id BIGSERIAL PRIMARY KEY,
    run_id BIGINT REFERENCES extraction_runs (run_id),
    status VARCHAR(40) NOT NULL,
    message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS entity_relations (
    relation_id BIGSERIAL PRIMARY KEY,
    head_id VARCHAR(20) NOT NULL REFERENCES dim_entities (entity_id),
    relation_type VARCHAR(40) NOT NULL CHECK (relation_type IN (
        'COMMANDED', 'PARTICIPATED_IN', 'OPPOSED_IN', 'TOOK_PLACE_AT',
        'OCCURRED_DURING', 'EMPLOYED_STRATEGY', 'LEFT_HERITAGE', 'SUPPORTS'
    )),
    tail_id VARCHAR(20) NOT NULL REFERENCES dim_entities (entity_id),
    source_chunk_ids TEXT[] NOT NULL DEFAULT '{}',
    evidence_count INT NOT NULL DEFAULT 0,
    quote TEXT,
    UNIQUE (head_id, relation_type, tail_id)
);

CREATE TABLE IF NOT EXISTS entity_measurements (
    measurement_id BIGSERIAL PRIMARY KEY,
    entity_id VARCHAR(20) NOT NULL REFERENCES dim_entities (entity_id),
    raw_expression VARCHAR(255) NOT NULL,
    quantity_raw NUMERIC(14, 4),
    unit_raw VARCHAR(50),
    target_type VARCHAR(40),
    normalized_value_si NUMERIC(18, 4),
    si_unit VARCHAR(20),
    conversion_note TEXT
);

CREATE OR REPLACE FUNCTION next_entity_id(p_type text)
RETURNS text
LANGUAGE plpgsql
AS $$
DECLARE
    n bigint;
BEGIN
    IF p_type = 'Person' THEN
        n := nextval('seq_person');
        RETURN 'P' || lpad(n::text, 5, '0');
    ELSIF p_type = 'Event' THEN
        n := nextval('seq_event');
        RETURN 'EV' || lpad(n::text, 5, '0');
    ELSIF p_type = 'Group' THEN
        n := nextval('seq_group');
        RETURN 'GRP' || lpad(n::text, 4, '0');
    ELSIF p_type = 'Place' THEN
        n := nextval('seq_place');
        RETURN 'LOC' || lpad(n::text, 4, '0');
    ELSIF p_type = 'TimeSpan' THEN
        n := nextval('seq_time');
        RETURN 'TIM' || lpad(n::text, 4, '0');
    ELSIF p_type = 'Artifact' THEN
        n := nextval('seq_artifact');
        RETURN 'ART' || lpad(n::text, 4, '0');
    ELSIF p_type = 'Concept' THEN
        n := nextval('seq_concept');
        RETURN 'CON' || lpad(n::text, 4, '0');
    ELSIF p_type = 'Source' THEN
        n := nextval('seq_source');
        RETURN 'SRC' || lpad(n::text, 4, '0');
    END IF;
    RAISE EXCEPTION 'entity_type không hợp lệ: %', p_type;
END;
$$;

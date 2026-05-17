CREATE TABLE repositories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    github_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE scans (
    id SERIAL PRIMARY KEY,
    repo_id INTEGER REFERENCES repositories(id),
    sha TEXT NOT NULL,
    status TEXT NOT NULL,
    duration_seconds INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE vulnerabilities (
    id SERIAL PRIMARY KEY,
    scan_id INTEGER REFERENCES scans(id),
    severity TEXT,
    package_name TEXT,
    vuln_id TEXT,
    fixed_version TEXT
);
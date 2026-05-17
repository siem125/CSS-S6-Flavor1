"use client";

import { useEffect, useMemo, useState } from "react";

import RepoFilter from "@/app/components/RepoFilter";
import ScanTable from "@/app/components/ScanTable";

type Scan = {
  id: number;
  repo: { id: number; name: string; url: string };
  sha: string;
  event: string;
  status: string;
  block: boolean;
  reason?: string;
  vulnerability_count: number;
  duration: number;
  created_at: string;
};

export default function Home() {
  const [scans, setScans] = useState<Scan[]>([]);
  const [selectedRepo, setSelectedRepo] = useState("all");

  useEffect(() => {
    fetch("http://localhost:8000/scans") // you’ll need this endpoint
      .then((res) => res.json())
      .then(setScans);
  }, []);

  const repositories = useMemo(() => {
    return Array.from(new Set(scans.map((s) => s.repo.name)));
  }, [scans]);

  const filteredScans = useMemo(() => {
    if (selectedRepo === "all") return scans;

    return scans.filter((s) => s.repo.name === selectedRepo);
  }, [scans, selectedRepo]);

  return (
    <main className="min-h-screen bg-zinc-950 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-4xl font-bold">
            Security Dashboard
          </h1>

          <RepoFilter
            repositories={repositories}
            selected={selectedRepo}
            onChange={setSelectedRepo}
          />
        </div>

        <div className="grid grid-cols-4 gap-4">
          <div className="bg-zinc-900 p-6 rounded-xl">
            <h2 className="text-sm text-zinc-400">Repositories</h2>
            <p className="text-3xl font-bold">12</p>
          </div>

          <div className="bg-zinc-900 p-6 rounded-xl">
            <h2 className="text-sm text-zinc-400">Critical Vulnerabilities</h2>
            <p className="text-3xl font-bold text-red-500">4</p>
          </div>

          <div className="bg-zinc-900 p-6 rounded-xl">
            <h2 className="text-sm text-zinc-400">Failed Scans</h2>
            <p className="text-3xl font-bold text-yellow-500">2</p>
          </div>

          <div className="bg-zinc-900 p-6 rounded-xl">
            <h2 className="text-sm text-zinc-400">Successful Scans</h2>
            <p className="text-3xl font-bold text-green-500">10</p>
          </div>
        </div>

        <ScanTable scans={filteredScans} />
      </div>
    </main>
  );
}
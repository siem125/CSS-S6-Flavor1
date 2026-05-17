import { notFound } from "next/navigation";

import StatusBadge from "@/app/components/StatusBadge";
import SeverityBadge from "@/app/components/SeverityBadge";
import VulnerabilityList from "@/app/components/VulnerabilityList";

type Props = {
  params: {
    id: string;
  };
};

async function getRepo(id: string) {
  const res = await fetch(`http://backend:8000/repos/${id}`, {
    cache: "no-store",
  });

  if (!res.ok) return null;

  return res.json();
}

export default async function RepoDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const repo = await getRepo(id);

  if (!repo) return notFound();

  const latestScan = repo.scans[0];

  return (
    <main className="min-h-screen bg-zinc-950 text-white p-8">
      <div className="max-w-5xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">
            {repo.name}
          </h1>

          <p className="text-zinc-400">{repo.url}</p>
        </div>

        {/* STATS */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-zinc-900 rounded-2xl p-6">
            <h2 className="text-sm text-zinc-400 mb-2">
              Scans
            </h2>
            <p className="text-2xl">{repo.scans.length}</p>
          </div>

          <div className="bg-zinc-900 rounded-2xl p-6">
            <h2 className="text-sm text-zinc-400 mb-2">
              Latest Scan Status
            </h2>
            <p className="text-2xl">
              {latestScan?.status}
            </p>
          </div>

          <div className="bg-zinc-900 rounded-2xl p-6">
            <h2 className="text-sm text-zinc-400 mb-2">
              Total Vulnerabilities
            </h2>
            <p className="text-2xl">
              {repo.scans.reduce(
                (acc, s) => acc + s.vulnerability_count,
                0
              )}
            </p>
          </div>
        </div>

        {/* SCANS + VULNERABILITIES */}
        <div className="space-y-6">
          <VulnerabilityList vulnerabilities={latestScan.vulnerabilities} />
        </div>
      </div>
    </main>
  );
}
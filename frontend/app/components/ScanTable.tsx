import Link from "next/link";
import StatusBadge from "./StatusBadge";

type Repo = {
  id: number,
  name: string,
  url: string
}

type Scan = {
  id: number;
  repo: Repo;
  date: string;
  passed: boolean;
};

type Props = {
  scans: Scan[];
};

export default function ScanTable({ scans }: Props) {
  return (
    <div className="bg-zinc-900 rounded-2xl overflow-hidden">
      <table className="w-full">
        <thead className="bg-zinc-800 text-zinc-400 text-sm">
          <tr>
            <th className="text-left p-4">Repository</th>
            <th className="text-left p-4">Date</th>
            <th className="text-left p-4">Status</th>
            <th className="text-left p-4">Details</th>
          </tr>
        </thead>

        <tbody>
          {scans.map((scan) => (
            <tr
              key={scan.id}
              className="border-t border-zinc-800"
            >
              <td className="p-4">{scan.repo.name}</td>
              <td className="p-4">{scan.date}</td>
              <td className="p-4">
                <StatusBadge passed={scan.passed} />
              </td>
              <td className="p-4">
                <Link
                  href={`/scans/${scan.id}`}
                  className="text-blue-400 hover:underline"
                >
                  View
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
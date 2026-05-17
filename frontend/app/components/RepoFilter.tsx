type Props = {
  repositories: string[];
  selected: string;
  onChange: (value: string) => void;
};

export default function RepoFilter({
  repositories,
  selected,
  onChange,
}: Props) {
  return (
    <select
      value={selected}
      onChange={(e) => onChange(e.target.value)}
      className="bg-zinc-900 border border-zinc-700 rounded-lg px-4 py-2"
    >
      <option value="all">All repositories</option>

      {repositories.map((repo) => (
        <option key={repo} value={repo}>
          {repo}
        </option>
      ))}
    </select>
  );
}
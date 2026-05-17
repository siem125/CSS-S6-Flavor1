type Props = {
  passed: boolean;
};

export default function StatusBadge({ passed }: Props) {
  return (
    <span
      className={`px-3 py-1 rounded-full text-sm font-medium ${
        passed
          ? "bg-green-500/20 text-green-400"
          : "bg-red-500/20 text-red-400"
      }`}
    >
      {passed ? "PASS" : "FAIL"}
    </span>
  );
}
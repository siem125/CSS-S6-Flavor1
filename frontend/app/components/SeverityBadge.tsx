type Props = {
  severity: string;
};

export default function SeverityBadge({
  severity,
}: Props) {
  const colors: Record<string, string> = {
    LOW: "bg-blue-500/20 text-blue-400",
    MEDIUM: "bg-yellow-500/20 text-yellow-400",
    HIGH: "bg-orange-500/20 text-orange-400",
    CRITICAL: "bg-red-500/20 text-red-400",
  };

  return (
    <span
      className={`px-3 py-1 rounded-full text-sm font-medium ${
        colors[severity]
      }`}
    >
      {severity}
    </span>
  );
}
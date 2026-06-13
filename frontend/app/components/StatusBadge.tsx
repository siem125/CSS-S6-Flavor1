type Props = {
  block: boolean;
};

export default function StatusBadge({ block }: Props) {
  return (
    <span
      className={`px-3 py-1 rounded-full text-sm font-medium ${
        !block
          ? "bg-green-500/20 text-green-400"
          : "bg-red-500/20 text-red-400"
      }`}
    >
      {!block ? "Success" : "Failed"}
    </span>
  );
}
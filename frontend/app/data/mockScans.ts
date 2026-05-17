export const mockScans = [
  {
    id: 1,
    repository: "security-api",
    date: "2026-05-10 14:20",
    passed: true,
    commitSha: "a1b2c3d",
    duration: 12,
    vulnerabilities: [],
  },
  {
    id: 2,
    repository: "frontend-dashboard",
    date: "2026-05-10 14:25",
    passed: false,
    commitSha: "d4e5f6g",
    duration: 18,
    vulnerabilities: [
      {
        package: "lodash",
        severity: "HIGH",
      },
      {
        package: "requests",
        severity: "CRITICAL",
      },
    ],
  },
  {
    id: 3,
    repository: "scanner-worker",
    date: "2026-05-10 14:30",
    passed: true,
    commitSha: "h7i8j9k",
    duration: 8,
    vulnerabilities: [],
  },
];
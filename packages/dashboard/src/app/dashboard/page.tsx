export default function DashboardPage() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold text-teal-400">Golden Hour Dashboard</h1>
      <p className="mt-2 text-slate-400">Supervisor overview — real-time patient monitoring</p>
      <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-4">
        <StatCard label="Total Assessments" value="—" />
        <StatCard label="Critical Alerts" value="—" danger />
        <StatCard label="Avg Response Time" value="—" />
        <StatCard label="Active Facilities" value="—" />
      </div>
    </main>
  );
}

function StatCard({
  label,
  value,
  danger,
}: {
  label: string;
  value: string;
  danger?: boolean;
}) {
  return (
    <div
      className={`rounded-xl p-6 ${
        danger ? 'bg-rose-900/30 border border-rose-500/30' : 'bg-slate-800'
      }`}
    >
      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-1 text-2xl font-bold">{value}</p>
    </div>
  );
}

import { useState, useEffect } from 'react';
import Card from '../shared/Card';
import Loader from '../shared/Loader';
import api from '../../utils/api';
import { Users, BookOpen, TrendingUp, Target, BarChart3, PieChart } from 'lucide-react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const AdminDashboard = () => {
    const [stats, setStats] = useState({
        total_students: 0,
        total_tasks: 0,
        active_users: 0,
        ai_interactions: 0,
        total_students_accessed: 0,
        student_statuses: [],
        performance_history: {
            days: { labels: [], data: [] },
            months: { labels: [], data: [] },
            years: { labels: [], data: [] }
        },
        common_problems: [],
        high_requirements: []
    });
    const [loading, setLoading] = useState(true);
    const [timeframe, setTimeframe] = useState('months');

    useEffect(() => {
        const fetchAdminStats = async () => {
            setLoading(true);
            try {
                const response = await api.get('/api/stats/admin');
                setStats(response.data);
            } catch (err) {
                console.error("Failed to fetch admin stats", err);
            } finally {
                setLoading(false);
            }
        };
        fetchAdminStats();
    }, []);

    const performanceChartData = {
        labels: stats.performance_history[timeframe].labels,
        datasets: [{
            label: 'Total Tasks Completed',
            data: stats.performance_history[timeframe].data,
            backgroundColor: 'rgba(79, 70, 229, 0.4)',
            borderColor: 'rgb(79, 70, 229)',
            borderWidth: 2,
            tension: 0.3,
            fill: true
        }]
    };

    if (loading) return <Loader text="Loading admin insights..." />;

    return (
        <div className="max-w-7xl mx-auto py-4">
            <div className="mb-10 animate-fade-in flex justify-between items-end">
                <div>
                    <h1 className="text-4xl font-extrabold text-slate-900 mb-2 tracking-tight">
                        Admin Control Center
                    </h1>
                    <p className="text-slate-500 font-medium"> Comprehensive platform analytics and student performance oversight </p>
                </div>
                <div className="bg-white p-1 rounded-xl shadow-sm border border-slate-200">
                    <button
                        onClick={() => setTimeframe('days')}
                        className={`px-4 py-2 rounded-lg text-sm font-bold transition-all ${timeframe === 'days' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-50'}`}
                    >Days</button>
                    <button
                        onClick={() => setTimeframe('months')}
                        className={`mx-1 px-4 py-2 rounded-lg text-sm font-bold transition-all ${timeframe === 'months' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-50'}`}
                    >Months</button>
                    <button
                        onClick={() => setTimeframe('years')}
                        className={`px-4 py-2 rounded-lg text-sm font-bold transition-all ${timeframe === 'years' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-50'}`}
                    >Years</button>
                </div>
            </div>

            {/* Key Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-10">
                <Card className="border-t-4 border-blue-500 shadow-sm">
                    <p className="text-xs font-bold text-slate-400 uppercase mb-1">Total Students</p>
                    <p className="text-3xl font-black text-slate-900">{stats.total_students}</p>
                    <div className="mt-4 flex items-center text-blue-600">
                        <Users className="w-4 h-4 mr-1" />
                        <span className="text-xs font-bold">Registration Base</span>
                    </div>
                </Card>

                <Card className="border-t-4 border-green-500 shadow-sm">
                    <p className="text-xs font-bold text-slate-400 uppercase mb-1">Accessed System</p>
                    <p className="text-3xl font-black text-slate-900">{stats.total_students_accessed}</p>
                    <div className="mt-4 flex items-center text-green-600">
                        <Target className="w-4 h-4 mr-1" />
                        <span className="text-xs font-bold">{Math.round((stats.total_students_accessed / stats.total_students) * 100)}% Reach</span>
                    </div>
                </Card>

                <Card className="border-t-4 border-purple-500 shadow-sm">
                    <p className="text-xs font-bold text-slate-400 uppercase mb-1">Currently Active</p>
                    <p className="text-3xl font-black text-slate-900">{stats.active_users}</p>
                    <div className="mt-4 flex items-center text-purple-600">
                        <TrendingUp className="w-4 h-4 mr-1" />
                        <span className="text-xs font-bold">Live Users</span>
                    </div>
                </Card>

                <Card className="border-t-4 border-orange-500 shadow-sm">
                    <p className="text-xs font-bold text-slate-400 uppercase mb-1">Total Tasks</p>
                    <p className="text-3xl font-black text-slate-900">{stats.total_tasks}</p>
                    <div className="mt-4 flex items-center text-orange-600">
                        <BookOpen className="w-4 h-4 mr-1" />
                        <span className="text-xs font-bold">Activity Log</span>
                    </div>
                </Card>

                <Card className="border-t-4 border-pink-500 shadow-sm">
                    <p className="text-xs font-bold text-slate-400 uppercase mb-1">AI Interactions</p>
                    <p className="text-3xl font-black text-slate-900">{stats.ai_interactions}</p>
                    <div className="mt-4 flex items-center text-pink-600">
                        <BarChart3 className="w-4 h-4 mr-1" />
                        <span className="text-xs font-bold">Mentor Usage</span>
                    </div>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">
                {/* Performance History Chart */}
                <div className="lg:col-span-2">
                    <Card title={`Performance Overview (${timeframe.charAt(0).toUpperCase() + timeframe.slice(1)})`} icon={<BarChart3 className="text-indigo-600" />}>
                        <div className="h-80 mt-6">
                            <Bar
                                data={performanceChartData}
                                options={{
                                    responsive: true,
                                    maintainAspectRatio: false,
                                    plugins: { legend: { display: false } },
                                    scales: {
                                        y: { grid: { color: '#f1f5f9' }, border: { display: false } },
                                        x: { grid: { display: false }, border: { display: false } }
                                    }
                                }}
                            />
                        </div>
                    </Card>
                </div>

                {/* High Requirements & Problems */}
                <div className="space-y-8">
                    <Card title="Common Hurdles" icon={<PieChart className="text-rose-500" />}>
                        <div className="mt-4 space-y-4">
                            {stats.common_problems.length > 0 ? stats.common_problems.map((prob, i) => (
                                <div key={i} className="flex justify-between items-center bg-rose-50 p-3 rounded-xl border border-rose-100">
                                    <span className="text-sm font-bold text-rose-900">{prob.problem}</span>
                                    <span className="bg-rose-500 text-white text-xs px-2 py-1 rounded-lg font-black">{prob.count} pending</span>
                                </div>
                            )) : (
                                <p className="text-slate-400 text-sm italic">No significant problems identified.</p>
                            )}
                        </div>
                    </Card>

                    <Card title="High Requirements" icon={<TrendingUp className="text-cyan-500" />}>
                        <div className="mt-4 flex flex-wrap gap-2">
                            {stats.high_requirements.map((req, i) => (
                                <span key={i} className="bg-cyan-50 text-cyan-700 px-3 py-1.5 rounded-full text-xs font-bold border border-cyan-100 uppercase tracking-wider">
                                    {req}
                                </span>
                            ))}
                        </div>
                    </Card>
                </div>
            </div>

            {/* Student Status Table */}
            <Card title="Student Engagement Deep-Dive" icon={<Users className="text-indigo-600" />}>
                <div className="overflow-x-auto mt-6">
                    <table className="min-w-full divide-y divide-slate-200">
                        <thead>
                            <tr className="bg-slate-50">
                                <th className="px-6 py-4 text-left text-xs font-black text-slate-500 uppercase tracking-widest">Student</th>
                                <th className="px-6 py-4 text-left text-xs font-black text-slate-500 uppercase tracking-widest">Status</th>
                                <th className="px-6 py-4 text-left text-xs font-black text-slate-500 uppercase tracking-widest">Logins</th>
                                <th className="px-6 py-4 text-left text-xs font-black text-slate-500 uppercase tracking-widest">Last Activity</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-slate-100">
                            {stats.student_statuses.map((student, idx) => (
                                <tr key={idx} className="hover:bg-slate-50 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div className="text-sm font-bold text-slate-900">{student.name}</div>
                                        <div className="text-xs text-slate-500">{student.email}</div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-3 py-1 text-[10px] font-black rounded-full uppercase tracking-tighter ${student.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-400'
                                            }`}>
                                            {student.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-black text-slate-700">
                                        {student.login_count}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-xs font-medium text-slate-500">
                                        {student.last_login ? new Date(student.last_login).toLocaleString() : 'Never'}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </Card>
        </div>
    );
};

export default AdminDashboard;

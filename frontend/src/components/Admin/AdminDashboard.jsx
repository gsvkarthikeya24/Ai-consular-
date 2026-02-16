import { useState, useEffect } from 'react';
import Navbar from '../shared/Navbar';
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
        ai_interactions: 0
    });
    const [loading, setLoading] = useState(true);

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

    const chartData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [{
            label: 'System Engagement',
            data: [stats.total_tasks * 0.2, stats.total_tasks * 0.5, stats.total_tasks * 0.8, stats.total_tasks, stats.total_tasks * 1.2],
            backgroundColor: 'rgba(79, 70, 229, 0.6)',
        }]
    };

    if (loading) return <Loader text="Loading admin insights..." />;

    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="mb-8 animate-fade-in flex justify-between items-end">
                    <div>
                        <h1 className="text-3xl font-extrabold text-gray-900 mb-2">
                            Admin Dashboard
                        </h1>
                        <p className="text-gray-600"> Platform analytics and student engagement insights </p>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <Card hoverable className="border-l-4 border-blue-500">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs font-bold text-gray-500 uppercase mb-1">Total Students</p>
                                <p className="text-3xl font-extrabold text-gray-900">{stats.total_students}</p>
                            </div>
                            <div className="p-3 bg-blue-50 rounded-2xl">
                                <Users className="w-8 h-8 text-blue-600" />
                            </div>
                        </div>
                    </Card>

                    <Card hoverable className="border-l-4 border-green-500">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs font-bold text-gray-500 uppercase mb-1">Total Tasks</p>
                                <p className="text-3xl font-extrabold text-gray-900">{stats.total_tasks}</p>
                            </div>
                            <div className="p-3 bg-green-50 rounded-2xl">
                                <BookOpen className="w-8 h-8 text-green-600" />
                            </div>
                        </div>
                    </Card>

                    <Card hoverable className="border-l-4 border-purple-500">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs font-bold text-gray-500 uppercase mb-1">Active Users</p>
                                <p className="text-3xl font-extrabold text-gray-900">{stats.active_users}</p>
                            </div>
                            <div className="p-3 bg-purple-50 rounded-2xl">
                                <TrendingUp className="w-8 h-8 text-purple-600" />
                            </div>
                        </div>
                    </Card>

                    <Card hoverable className="border-l-4 border-orange-500">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs font-bold text-gray-500 uppercase mb-1">AI Interactions</p>
                                <p className="text-3xl font-extrabold text-gray-900">{stats.ai_interactions}</p>
                            </div>
                            <div className="p-3 bg-orange-50 rounded-2xl">
                                <Target className="w-8 h-8 text-orange-600" />
                            </div>
                        </div>
                    </Card>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <Card title="Activity Growth" icon={<BarChart3 className="text-indigo-600" />}>
                        <div className="h-64 mt-4">
                            <Bar
                                data={chartData}
                                options={{
                                    responsive: true,
                                    maintainAspectRatio: false,
                                    plugins: { legend: { display: false } }
                                }}
                            />
                        </div>
                    </Card>

                    <Card title="Engagement Split" icon={<PieChart className="text-pink-600" />}>
                        <div className="h-64 mt-4 flex justify-center">
                            <Pie
                                data={{
                                    labels: ['Career Guidance', 'Resume Builder', 'AI Mentor', 'Task Help'],
                                    datasets: [{
                                        data: [35, 25, 20, 20],
                                        backgroundColor: [
                                            'rgba(79, 70, 229, 0.7)',
                                            'rgba(16, 185, 129, 0.7)',
                                            'rgba(245, 158, 11, 0.7)',
                                            'rgba(236, 72, 153, 0.7)'
                                        ]
                                    }]
                                }}
                                options={{ responsive: true, maintainAspectRatio: false }}
                            />
                        </div>
                    </Card>
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;

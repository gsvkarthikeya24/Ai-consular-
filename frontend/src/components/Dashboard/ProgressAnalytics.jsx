import { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    PointElement,
    LineElement,
    RadialLinearScale,
    Filler
} from 'chart.js';
import { Bar, Radar, Line } from 'react-chartjs-2';
import { TrendingUp, Award, Target, BookOpen, Loader2 } from 'lucide-react';
import api from '../../utils/api';
import Card from '../shared/Card';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    RadialLinearScale,
    Filler,
    Title,
    Tooltip,
    Legend
);

const ProgressAnalytics = () => {
    const [loading, setLoading] = useState(true);
    const [taskStats, setTaskStats] = useState({ labels: [], datasets: [] });
    const [skillStats, setSkillStats] = useState({ labels: [], datasets: [] });

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                // Fetch tasks for analytics
                const taskResponse = await api.get('/api/tasks');
                const tasks = taskResponse.data;

                // Group by subject
                const subjectCounts = {};
                tasks.forEach(t => {
                    subjectCounts[t.subject] = (subjectCounts[t.subject] || 0) + 1;
                });

                setTaskStats({
                    labels: Object.keys(subjectCounts),
                    datasets: [{
                        label: 'Tasks per Subject',
                        data: Object.values(subjectCounts),
                        backgroundColor: 'rgba(79, 70, 229, 0.6)',
                        borderColor: 'rgb(79, 70, 229)',
                        borderWidth: 1,
                        borderRadius: 8
                    }]
                });

                // Mocking skill analytics based on interests and tasks
                setSkillStats({
                    labels: ['Technical Skills', 'Problem Solving', 'Communication', 'Consistency', 'Project Experience'],
                    datasets: [{
                        label: 'Current Level',
                        data: [75, 60, 45, 80, 55],
                        backgroundColor: 'rgba(16, 185, 129, 0.2)',
                        borderColor: 'rgb(16, 185, 129)',
                        pointBackgroundColor: 'rgb(16, 185, 129)',
                        borderWidth: 2
                    }]
                });

            } catch (err) {
                console.error("Failed to fetch analytics data", err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center py-20">
                <Loader2 className="w-12 h-12 text-primary-600 animate-spin mb-4" />
                <p className="text-gray-600 font-medium">Crunching your progress data...</p>
            </div>
        );
    }

    return (
        <div className="max-w-6xl mx-auto py-8 px-4">
            <div className="mb-8">
                <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Progress Analytics</h1>
                <p className="text-gray-600">Visual mapping of your academic performance and career readiness.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                <Card title="Academic Task Distribution" icon={<BookOpen className="text-blue-500" />}>
                    <div className="h-64">
                        <Bar
                            data={taskStats}
                            options={{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {
                                    legend: { display: false },
                                    tooltip: {
                                        backgroundColor: 'rgba(17, 24, 39, 0.9)',
                                        padding: 12,
                                        borderRadius: 12
                                    }
                                },
                                scales: {
                                    y: { beginAtZero: true, ticks: { stepSize: 1 } },
                                    x: { grid: { display: false } }
                                }
                            }}
                        />
                    </div>
                    <p className="text-xs text-center text-gray-400 mt-4">Distribution of your tasks across core subjects</p>
                </Card>

                <Card title="Skill Proficiency Radar" icon={<Target className="text-emerald-500" />}>
                    <div className="h-64 flex justify-center">
                        <Radar
                            data={skillStats}
                            options={{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {
                                    legend: { display: false }
                                },
                                scales: {
                                    r: {
                                        min: 0,
                                        max: 100,
                                        ticks: { display: false },
                                        grid: { color: 'rgba(229, 231, 235, 1)' },
                                        angleLines: { color: 'rgba(229, 231, 235, 1)' },
                                        pointLabels: {
                                            font: { size: 11, weight: '600' },
                                            color: '#4B5563'
                                        }
                                    }
                                }
                            }}
                        />
                    </div>
                </Card>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-gradient-to-br from-primary-600 to-indigo-700 p-6 rounded-3xl text-white shadow-xl">
                    <div className="flex justify-between items-start mb-4">
                        <TrendingUp className="w-8 h-8 opacity-50" />
                        <span className="bg-white/20 px-2 py-1 rounded-lg text-xs font-bold">+12% this month</span>
                    </div>
                    <h3 className="text-lg font-bold">Career Readiness</h3>
                    <div className="mt-2 flex items-baseline gap-2">
                        <span className="text-4xl font-extrabold">65</span>
                        <span className="text-primary-100 text-sm">/ 100</span>
                    </div>
                    <div className="mt-4 w-full bg-white/20 h-2 rounded-full overflow-hidden">
                        <div className="bg-white h-full" style={{ width: '65%' }}></div>
                    </div>
                </div>

                <div className="bg-white border border-gray-200 p-6 rounded-3xl shadow-sm hover:border-emerald-200 transition-colors">
                    <div className="flex justify-between items-start mb-4">
                        <Award className="w-8 h-8 text-emerald-500" />
                    </div>
                    <h3 className="text-lg font-bold text-gray-900">Consistency Score</h3>
                    <div className="mt-2 flex items-baseline gap-2">
                        <span className="text-4xl font-extrabold text-emerald-600">8.4</span>
                        <span className="text-gray-400 text-sm">/ 10</span>
                    </div>
                    <p className="mt-2 text-xs text-gray-500">Based on task completion vs deadlines</p>
                </div>

                <div className="bg-white border border-gray-200 p-6 rounded-3xl shadow-sm">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">AI Analysis</h3>
                    <div className="space-y-3">
                        <div className="p-3 bg-blue-50 text-blue-700 rounded-2xl text-xs leading-relaxed border border-blue-100 italic">
                            "You are excelling in Python and DSA. Focusing more on System Design could significantly boost your job readiness."
                        </div>
                        <button className="w-full py-2 bg-gray-50 text-gray-600 rounded-xl text-xs font-bold hover:bg-gray-100">
                            Get Full AI Audit
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProgressAnalytics;

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, Plus, Filter, Search, ChevronRight, Clock, CheckCircle2, AlertCircle } from 'lucide-react';
import api from '../../utils/api';
import Card from '../shared/Card';
import Button from '../shared/Button';
import Loader from '../shared/Loader';

const TaskList = () => {
    const navigate = useNavigate();
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all');
    const [search, setSearch] = useState('');

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        setLoading(true);
        try {
            const response = await api.get('/api/tasks');
            setTasks(response.data);
        } catch (err) {
            console.error("Failed to fetch tasks", err);
        } finally {
            setLoading(false);
        }
    };

    const filteredTasks = tasks.filter(task => {
        const matchesFilter = filter === 'all' || task.status === filter;
        const matchesSearch = task.title.toLowerCase().includes(search.toLowerCase()) ||
            task.subject.toLowerCase().includes(search.toLowerCase());
        return matchesFilter && matchesSearch;
    });

    const getStatusIcon = (status) => {
        switch (status) {
            case 'completed': return <CheckCircle2 className="w-5 h-5 text-green-500" />;
            case 'in-progress': return <Clock className="w-5 h-5 text-orange-500" />;
            default: return <AlertCircle className="w-5 h-5 text-gray-400" />;
        }
    };

    const getStatusClass = (status) => {
        switch (status) {
            case 'completed': return 'bg-green-100 text-green-700';
            case 'in-progress': return 'bg-orange-100 text-orange-700';
            default: return 'bg-gray-100 text-gray-700';
        }
    };

    if (loading) return <Loader text="Fetching your tasks..." />;

    return (
        <div className="max-w-6xl mx-auto py-8 px-4">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">My Academic Tasks</h1>
                    <p className="text-gray-400">Track and manage your assignments, homework, and projects.</p>
                </div>
                <Button className="flex items-center gap-2">
                    <Plus className="w-5 h-5" /> New Task
                </Button>
            </div>

            {/* Filters & Search */}
            <div className="flex flex-col md:flex-row gap-4 mb-8">
                <div className="flex-grow relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                        type="text"
                        placeholder="Search by title or subject..."
                        className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 outline-none"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                </div>
                <div className="flex items-center gap-2">
                    <Filter className="text-gray-400 w-5 h-5" />
                    <select
                        className="border border-gray-200 rounded-xl px-4 py-2 outline-none focus:ring-2 focus:ring-primary-500"
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                    >
                        <option value="all">All Status</option>
                        <option value="pending">Pending</option>
                        <option value="in-progress">In Progress</option>
                        <option value="completed">Completed</option>
                    </select>
                </div>
            </div>

            {/* Task Grid */}
            {filteredTasks.length > 0 ? (
                <div className="grid grid-cols-1 gap-4">
                    {filteredTasks.map((task) => (
                        <div
                            key={task.id}
                            onClick={() => navigate(`/tasks/${task.id}`)}
                            className="bg-white border border-gray-200 rounded-2xl p-4 flex items-center justify-between hover:shadow-md transition-shadow cursor-pointer group animate-fade-in"
                        >
                            <div className="flex items-center gap-4">
                                <div className={`p-3 rounded-xl ${task.type === 'final-year-project' ? 'bg-purple-100 text-purple-600' :
                                    task.type === 'mini-project' ? 'bg-indigo-100 text-indigo-600' :
                                        'bg-blue-100 text-blue-600'
                                    }`}>
                                    <BookOpen className="w-6 h-6" />
                                </div>
                                <div>
                                    <h3 className="font-bold text-gray-900 group-hover:text-primary-600 transition-colors uppercase text-xs tracking-wider mb-1">
                                        {task.subject}
                                    </h3>
                                    <p className="font-semibold text-gray-800 text-lg mb-1">{task.title}</p>
                                    <div className="flex items-center gap-3">
                                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${getStatusClass(task.status)}`}>
                                            {task.status}
                                        </span>
                                        <span className="text-xs text-gray-500 capitalize">{task.type.replace('-', ' ')}</span>
                                        {task.ai_assistance_used && (
                                            <span className="flex items-center gap-1 text-xs text-primary-600 font-medium">
                                                <div className="w-1 h-1 bg-primary-600 rounded-full"></div>
                                                AI Assisted
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="hidden md:block text-right mr-4">
                                    <p className="text-xs text-gray-400 mb-1">Created on</p>
                                    <p className="text-sm font-medium text-gray-700">{new Date(task.created_at).toLocaleDateString()}</p>
                                </div>
                                <div className="p-2 bg-gray-50 rounded-full group-hover:bg-primary-50 transition-colors">
                                    <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-primary-600" />
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="text-center py-20 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200">
                    <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold text-gray-700 mb-2">No tasks found</h3>
                    <p className="text-gray-500 max-w-md mx-auto">
                        Seems like you don't have any tasks matching your criteria. Time to add one or celebrate your free time!
                    </p>
                </div>
            )}
        </div>
    );
};

export default TaskList;

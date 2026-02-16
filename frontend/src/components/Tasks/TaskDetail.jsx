import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Bot, Send, ArrowLeft, CheckCircle2, Clock, AlertCircle, Sparkles, BookOpen } from 'lucide-react';
import api from '../../utils/api';
import Card from '../shared/Card';
import Button from '../shared/Button';
import Loader from '../shared/Loader';

const TaskDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [task, setTask] = useState(null);
    const [loading, setLoading] = useState(true);
    const [assistLoading, setAssistLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const chatEndRef = useRef(null);

    useEffect(() => {
        fetchTask();
    }, [id]);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [chatHistory]);

    const fetchTask = async () => {
        setLoading(true);
        try {
            const response = await api.get(`/api/tasks/${id}`);
            const taskData = response.data;
            setTask(taskData);
            setChatHistory(taskData.conversation_history || []);
        } catch (err) {
            console.error("Failed to fetch task", err);
        } finally {
            setLoading(false);
        }
    };

    const handleAssist = async (e) => {
        e.preventDefault();
        if (!message.trim() || assistLoading) return;

        const userMsg = { role: 'user', content: message, timestamp: new Date().toISOString() };
        setChatHistory(prev => [...prev, userMsg]);
        const currentMsg = message;
        setMessage('');
        setAssistLoading(true);

        try {
            const response = await api.post(`/api/tasks/${id}/assist`, { message: currentMsg });
            setChatHistory(response.data.conversation_history);
        } catch (err) {
            console.error("Failed to get AI assistance", err);
        } finally {
            setAssistLoading(false);
        }
    };

    const markCompleted = async () => {
        try {
            await api.put(`/api/tasks/${id}/complete`);
            fetchTask();
        } catch (err) {
            console.error("Failed to complete task", err);
        }
    };

    if (loading) return <Loader text="Loading task details..." />;
    if (!task) return <div className="text-center py-20">Task not found</div>;

    return (
        <div className="max-w-6xl mx-auto py-8 px-4 flex flex-col lg:flex-row gap-8 min-h-[calc(100vh-100px)]">
            {/* Task Info & Content */}
            <div className="flex-grow space-y-6">
                <button
                    onClick={() => navigate('/tasks')}
                    className="flex items-center gap-2 text-gray-500 hover:text-primary-600 transition-colors mb-4"
                >
                    <ArrowLeft className="w-4 h-4" /> Back to Task List
                </button>

                <div className="flex justify-between items-start">
                    <div>
                        <div className="flex items-center gap-2 mb-2">
                            <span className="px-2 py-0.5 bg-blue-100 text-white-700 rounded-md text-[10px] font-bold uppercase tracking-wider">
                                {task.subject}
                            </span>
                            <span className="text-xs text-white-400 capitalize">• {task.type?.replace('-', ' ')}</span>
                        </div>
                        <h1 className="text-3xl font-bold text-white-900 mb-2">{task.title}</h1>
                    </div>
                    {task.status !== 'completed' && (
                        <Button onClick={markCompleted} className="bg-white-600 hover:bg-green-700">Mark Completed</Button>
                    )}
                </div>

                <Card className="prose max-w-none">
                    <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
                        <BookOpen className="w-5 h-5 text-primary-500" /> Task Description
                    </h3>
                    <div className="text-white-700 whitespace-pre-wrap leading-relaxed">
                        {task.description}
                    </div>
                </Card>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 bg-gray-50 rounded-2xl border border-white-100">
                        <p className="text-xs text-gray-400 mb-1 uppercase tracking-widest font-bold">Status</p>
                        <div className="flex items-center gap-2">
                            {task.status === 'completed' ? <CheckCircle2 className="w-4 h-4 text-green-500" /> :
                                task.status === 'in-progress' ? <Clock className="w-4 h-4 text-orange-500" /> :
                                    <AlertCircle className="w-4 h-4 text-gray-400" />}
                            <span className="font-semibold text-gray-800 capitalize">{task.status}</span>
                        </div>
                    </div>
                    <div className="p-4 bg-gray-50 rounded-2xl border border-gray-100">
                        <p className="text-xs text-gray-400 mb-1 uppercase tracking-widest font-bold">Difficulty</p>
                        <span className={`font-semibold capitalize ${task.difficulty === 'hard' ? 'text-red-500' :
                            task.difficulty === 'medium' ? 'text-orange-500' : 'text-green-500'
                            }`}>
                            {task.difficulty || 'Medium'}
                        </span>
                    </div>
                    <div className="p-4 bg-gray-50 rounded-2xl border border-gray-100">
                        <p className="text-xs text-gray-400 mb-1 uppercase tracking-widest font-bold">AI Help Used</p>
                        <span className="font-semibold text-gray-800">{task.ai_assistance_used ? 'Yes' : 'No'}</span>
                    </div>
                </div>
            </div>

            {/* AI Assistant Sidebar */}
            <div className="w-full lg:w-[400px] flex flex-col bg-white border border-white-200 rounded-3xl shadow-sm overflow-hidden sticky top-8 h-[calc(100vh-140px)]">
                <div className="p-4 bg-primary-600 text-white flex items-center gap-3">
                    <div className="p-2 bg-white/20 rounded-lg">
                        <Sparkles className="w-5 h-5" />
                    </div>
                    <div>
                        <h3 className="font-bold">AI Assignment Guide</h3>
                        <p className="text-[10px] text-primary-100">Concept clarity & guidance</p>
                    </div>
                </div>

                <div className="flex-grow overflow-y-auto p-4 space-y-4 bg-white-50">
                    {chatHistory.length === 0 ? (
                        <div className="text-center py-10">
                            <Bot className="w-12 h-12 text-white-300 mx-auto mb-3" />
                            <p className="text-sm text-gray-500 italic px-6">
                                Ask me anything about this task. I'll help you understand the core concepts without just giving you the answers!
                            </p>
                        </div>
                    ) : (
                        chatHistory.map((msg, i) => (
                            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[85%] p-3 rounded-2xl text-sm ${msg.role === 'user'
                                    ? 'bg-primary-600 text-white rounded-tr-none'
                                    : 'bg-white text-gray-800 border border-gray-100 rounded-tl-none shadow-sm'
                                    }`}>
                                    {msg.content}
                                </div>
                            </div>
                        ))
                    )}
                    {assistLoading && (
                        <div className="flex justify-start">
                            <div className="p-3 bg-white border border-gray-100 rounded-2xl shadow-sm rounded-tl-none">
                                <div className="flex gap-1">
                                    <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce"></span>
                                    <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                                    <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={chatEndRef} />
                </div>

                <form onSubmit={handleAssist} className="p-3 border-t border-gray-100">
                    <div className="flex gap-2 p-1 border border-gray-200 rounded-2xl focus-within:ring-2 focus-within:ring-primary-500 transition-all">
                        <input
                            type="text"
                            className="flex-grow px-3 py-2 text-xs outline-none bg-transparent"
                            placeholder="Ask for guidance..."
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            disabled={assistLoading}
                        />
                        <button
                            type="submit"
                            disabled={assistLoading || !message.trim()}
                            className="p-2 bg-primary-600 text-white rounded-xl hover:bg-primary-700 disabled:opacity-50 transition-colors"
                        >
                            <Send className="w-5 h-5" />
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default TaskDetail;

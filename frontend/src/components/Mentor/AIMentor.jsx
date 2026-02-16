import { useState, useEffect, useRef } from 'react';
import { Send, User, Bot, Loader2, Sparkles, Lightbulb, Quote } from 'lucide-react';
import api from '../../utils/api';
import Card from '../shared/Card';
import Button from '../shared/Button';

const AIMentor = () => {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am your AI Mentor. How can I help you today? I can provide academic guidance, career advice, or just some motivation!' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [motivation, setMotivation] = useState('');
    const [tips, setTips] = useState([]);
    const [fetchingMotivation, setFetchingMotivation] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        fetchMotivation();
        fetchTips();
    }, []);

    const fetchMotivation = async () => {
        setFetchingMotivation(true);
        try {
            const response = await api.get('/api/mentor/motivation');
            setMotivation(response.data.message);
        } catch (err) {
            console.error("Failed to fetch motivation", err);
        } finally {
            setFetchingMotivation(false);
        }
    };

    const fetchTips = async () => {
        try {
            const response = await api.get('/api/mentor/tips');
            setTips(response.data);
        } catch (err) {
            console.error("Failed to fetch tips", err);
        }
    };

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await api.post('/api/mentor/chat', {
                message: input,
                conversation_history: messages.slice(-5)
            });
            setMessages(prev => [...prev, { role: 'assistant', content: response.data.response }]);
        } catch (err) {
            setMessages(prev => [...prev, { role: 'assistant', content: "I'm sorry, I'm having trouble connecting right now. Let's try again in a moment." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-6xl mx-auto py-8 px-4 h-[calc(100vh-100px)] flex flex-col md:flex-row gap-6">
            {/* Sidebar - Tips & Motivation */}
            <div className="w-full md:w-80 flex flex-col gap-6 order-2 md:order-1 overflow-y-auto">
                <Card className="bg-surface/60 backdrop-blur-md border border-white/20 p-5">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="p-2 rounded-lg bg-yellow-500/20">
                            <Quote className="text-yellow-400 w-5 h-5" />
                        </div>
                        <h3 className="font-bold text-white text-lg tracking-tight">Daily Motivation</h3>
                    </div>
                    <div className="relative italic text-white">
                        {fetchingMotivation ? (
                            <div className="flex justify-center p-4">
                                <Loader2 className="w-6 h-6 animate-spin text-primary-400" />
                            </div>
                        ) : (
                            <>
                                <p className="leading-relaxed font-semibold">"{motivation || "The only way to do great work is to love what you do."}"</p>
                                <button
                                    onClick={fetchMotivation}
                                    className="mt-4 text-xs text-primary-300 hover:text-white font-bold flex items-center gap-1 transition-colors underline decoration-primary-500/50"
                                >
                                    <Sparkles className="w-3 h-3" /> Get another quote
                                </button>
                            </>
                        )}
                    </div>
                </Card>

                <Card className="bg-surface/60 backdrop-blur-md border border-white/20 p-5">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="p-2 rounded-lg bg-blue-500/20">
                            <Lightbulb className="text-blue-400 w-5 h-5" />
                        </div>
                        <h3 className="font-bold text-white text-lg tracking-tight">Productivity Tips</h3>
                    </div>
                    <div className="space-y-5">
                        {tips.map((tip, i) => (
                            <div key={i} className="border-b border-white/10 last:border-0 pb-4 last:pb-0">
                                <h4 className="text-sm font-bold text-white mb-1.5">{tip.title}</h4>
                                <p className="text-xs text-white leading-relaxed font-medium opacity-90">{tip.description}</p>
                            </div>
                        ))}
                    </div>
                </Card>
            </div>

            {/* Main Chat Area */}
            <div className="flex-grow flex flex-col bg-gray-900 rounded-2xl border border-white/20 shadow-2xl overflow-hidden order-1 md:order-2">
                {/* Chat Header */}
                <div className="p-4 border-b border-white/10 bg-white/10 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white shadow-lg shadow-primary-500/40">
                            <Bot className="w-6 h-6" />
                        </div>
                        <div>
                            <h2 className="font-bold text-white text-lg">AI Mentor</h2>
                            <p className="text-xs text-green-400 flex items-center gap-1 font-bold">
                                <span className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse shadow-[0_0_10px_rgba(34,197,94,0.8)]"></span>
                                Online and ready to help
                            </p>
                        </div>
                    </div>
                </div>

                {/* Messages Area */}
                <div className="flex-grow overflow-y-auto p-4 space-y-6 bg-gray-900/50">
                    {messages.map((msg, i) => (
                        <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
                            <div className={`flex items-start gap-3 max-w-[85%]`}>
                                {msg.role === 'assistant' && (
                                    <div className="w-9 h-9 rounded-full bg-primary-900 flex items-center justify-center shrink-0 border border-primary-500/50 mt-1">
                                        <Bot className="w-5 h-5 text-primary-400" />
                                    </div>
                                )}
                                <div className={`p-4 rounded-2xl shadow-lg text-[15px] leading-relaxed font-medium ${msg.role === 'user'
                                    ? 'bg-cyan-600 text-white rounded-tr-none shadow-cyan-500/20'
                                    : 'bg-slate-700 text-white border border-white/10 rounded-tl-none shadow-black/40'
                                    }`}>
                                    {msg.content}
                                </div>
                                {msg.role === 'user' && (
                                    <div className="w-9 h-9 rounded-full bg-slate-800 flex items-center justify-center shrink-0 border border-slate-600 mt-1">
                                        <User className="w-5 h-5 text-white" />
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="flex justify-start animate-fade-in">
                            <div className="flex items-start gap-2 max-w-[85%]">
                                <div className="w-8 h-8 rounded-full bg-primary-900/50 flex items-center justify-center shrink-0 border border-primary-500/30">
                                    <Bot className="w-4 h-4 text-primary-400" />
                                </div>
                                <div className="p-4 bg-gray-800 border border-white/10 rounded-2xl shadow-sm rounded-tl-none">
                                    <div className="flex gap-1">
                                        <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></span>
                                        <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                                        <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <form onSubmit={handleSend} className="p-4 border-t border-white/10 bg-white/5">
                    <div className="flex gap-2 p-1 border border-white/10 rounded-xl bg-gray-900/50 focus-within:ring-2 focus-within:ring-primary-500/50 focus-within:border-transparent transition-all">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type your question here (e.g., 'How to focus while studying?')"
                            className="flex-grow px-4 py-3 text-sm outline-none border-0 bg-transparent text-white placeholder-gray-500"
                            disabled={loading}
                        />
                        <button
                            type="submit"
                            disabled={loading || !input.trim()}
                            className="p-3 bg-primary-600 text-white rounded-lg hover:bg-primary-500 disabled:opacity-50 disabled:hover:bg-primary-600 transition-colors shadow-lg shadow-primary-600/20"
                        >
                            <Send className="w-5 h-5" />
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default AIMentor;

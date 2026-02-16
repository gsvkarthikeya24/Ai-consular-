import { useState, useEffect } from 'react';
import { Briefcase, MessageSquare, BookOpen, Star, RefreshCw, Loader2 } from 'lucide-react';
import api from '../../utils/api';
import Card from '../shared/Card';
import Button from '../shared/Button';

const InterviewPrep = () => {
    const [loading, setLoading] = useState(false);
    const [prepData, setPrepData] = useState(null);
    const [error, setError] = useState('');

    const fetchPrepData = async () => {
        setLoading(true);
        setError('');
        try {
            // This endpoint will be handled by the AI service via a specific route 
            // For now, we'll simulate the response if the route doesn't exist yet
            // or use a default domain like "Software Engineering"
            const response = await api.get('/api/career/domains/full_stack_developer');

            // Note: In a full implementation, we'd have a POST /api/interview/prep 
            // that takes a domain ID. For this demo, we'll use the AI service's 
            // internal logic which we already enhanced in the backend.

            // Simulating a response for the demo
            setTimeout(() => {
                setPrepData({
                    questions: [
                        "Explain the difference between process and thread.",
                        "What is ACID property in DBMS?",
                        "How does a hash map work internally?",
                        "What is the time complexity of various sorting algorithms?",
                        "Explain the concept of Virtual Memory."
                    ],
                    concepts: [
                        "Object Oriented Programming (Inheritance, Polymorphism)",
                        "Complexity Analysis (Big O)",
                        "System Design Basics",
                        "Normalization in Databases"
                    ],
                    behavioral: [
                        "Tell me about a challenging project you worked on.",
                        "How do you handle conflict in a team?"
                    ]
                });
                setLoading(false);
            }, 1000);

        } catch (err) {
            setError('Failed to fetch preparation guide. Please try again.');
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPrepData();
    }, []);

    return (
        <div className="max-w-5xl mx-auto py-8 px-4">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Interview Preparation Guide</h1>
                    <p className="text-gray-600">Master your technical and behavioral interviews with AI-curated content.</p>
                </div>
                <Button onClick={fetchPrepData} variant="outline" className="flex items-center gap-2">
                    <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} /> Refresh
                </Button>
            </div>

            {loading ? (
                <div className="flex flex-col items-center justify-center py-20">
                    <Loader2 className="w-12 h-12 text-primary-600 animate-spin mb-4" />
                    <p className="text-gray-600 font-medium">Curating interview questions for you...</p>
                </div>
            ) : error ? (
                <div className="p-4 bg-red-50 text-red-700 border border-red-200 rounded-xl">{error}</div>
            ) : prepData && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 animate-fade-in">
                    <Card title="Top Technical Questions" icon={<MessageSquare className="text-blue-500" />}>
                        <div className="space-y-4">
                            {prepData.questions.map((q, i) => (
                                <div key={i} className="flex gap-4 p-3 hover:bg-gray-50 rounded-xl transition-colors">
                                    <span className="flex items-center justify-center w-6 h-6 rounded-full bg-blue-100 text-blue-600 font-bold text-xs shrink-0">{i + 1}</span>
                                    <p className="text-sm text-gray-800 font-medium">{q}</p>
                                </div>
                            ))}
                        </div>
                    </Card>

                    <div className="space-y-8">
                        <Card title="Core Concepts to Review" icon={<BookOpen className="text-purple-500" />}>
                            <ul className="space-y-3">
                                {prepData.concepts.map((c, i) => (
                                    <li key={i} className="flex items-center gap-3 text-sm text-gray-700">
                                        <div className="w-1.5 h-1.5 rounded-full bg-purple-500"></div>
                                        {c}
                                    </li>
                                ))}
                            </ul>
                        </Card>

                        <Card title="Behavioral Tips" icon={<Star className="text-yellow-500" />}>
                            <div className="space-y-4">
                                {prepData.behavioral.map((b, i) => (
                                    <div key={i} className="p-4 bg-yellow-50 rounded-xl border border-yellow-100">
                                        <p className="text-sm text-gray-800 italic">"{b}"</p>
                                        <button className="mt-2 text-xs text-yellow-700 font-bold flex items-center gap-1">
                                            How to answer <RefreshCw className="w-3 h-3" />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </Card>
                    </div>

                    <Card className="md:col-span-2 bg-primary-600 text-white border-0 shadow-lg">
                        <div className="flex flex-col md:flex-row items-center justify-between gap-6 py-4">
                            <div className="flex items-center gap-4">
                                <div className="p-4 bg-white/20 rounded-2xl">
                                    <Briefcase className="w-10 h-10" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold mb-1">Mock Interview Mode</h3>
                                    <p className="text-primary-100 text-sm">Practice real-time with our AI and get instant feedback on your answers.</p>
                                </div>
                            </div>
                            <Button className="bg-white text-primary-600 hover:bg-primary-50 px-8 py-3 font-bold border-0 shadow-none">
                                Start Mock Interview
                            </Button>
                        </div>
                    </Card>
                </div>
            )}
        </div>
    );
};

export default InterviewPrep;

import { useState, useEffect } from 'react';
import { BookOpen, Award, TrendingUp, Clock, CheckCircle, XCircle, BarChart3, FileText, Video, ExternalLink, Library, Loader2, ChevronRight } from 'lucide-react';
import api from '../../utils/api';
import Card from '../UI/Card';

const GATEPrep = () => {
    const [activeTab, setActiveTab] = useState('practice'); // 'practice', 'progress', 'resources'
    const [questions, setQuestions] = useState([]);
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [showResult, setShowResult] = useState(false);
    const [result, setResult] = useState(null);

    const [progress, setProgress] = useState(null);
    const [resources, setResources] = useState([]);
    const [loading, setLoading] = useState(false);
    const [filter, setFilter] = useState({ subject: '', difficulty: '' });

    useEffect(() => {
        if (activeTab === 'practice') {
            fetchQuestions();
        } else if (activeTab === 'progress') {
            fetchProgress();
        } else if (activeTab === 'resources') {
            fetchResources();
        }
    }, [activeTab, filter]);

    const fetchQuestions = async () => {
        setLoading(true);
        try {
            const params = new URLSearchParams();
            if (filter.subject) params.append('subject', filter.subject);
            if (filter.difficulty) params.append('difficulty', filter.difficulty);
            params.append('limit', '10');

            const response = await api.get(`/api/gate/questions?${params}`);
            setQuestions(response.data);
            setCurrentQuestion(0);
            setSelectedAnswer(null);
            setShowResult(false);
        } catch (error) {
            console.error('Failed to fetch questions:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchProgress = async () => {
        setLoading(true);
        try {
            const response = await api.get('/api/gate/progress');
            setProgress(response.data);
        } catch (error) {
            console.error('Failed to fetch progress:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchResources = async () => {
        setLoading(true);
        try {
            const params = new URLSearchParams();
            if (filter.subject) params.append('subject', filter.subject);

            const response = await api.get(`/api/gate/resources?${params}`);
            setResources(response.data);
        } catch (error) {
            console.error('Failed to fetch resources:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmitAnswer = async () => {
        if (selectedAnswer === null) return;

        setLoading(true);
        try {
            const response = await api.post('/api/gate/submit-answer', {
                question_id: questions[currentQuestion].question_id,
                selected_answer: selectedAnswer,
                time_taken: 60 // You can track actual time
            });
            setResult(response.data);
            setShowResult(true);
        } catch (error) {
            console.error('Failed to submit answer:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleNextQuestion = () => {
        if (currentQuestion < questions.length - 1) {
            setCurrentQuestion(currentQuestion + 1);
            setSelectedAnswer(null);
            setShowResult(false);
            setResult(null);
        }
    };

    const getDifficultyColor = (difficulty) => {
        switch (difficulty?.toLowerCase()) {
            case 'easy': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
            case 'medium': return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
            case 'hard': return 'bg-rose-500/20 text-rose-400 border-rose-500/30';
            default: return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
        }
    };

    if (loading && questions.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh] animate-fade-in">
                <Loader2 className="w-12 h-12 text-primary animate-spin mb-4" />
                <p className="text-white font-medium">Loading GATE Preparation...</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-transparent p-4 sm:p-6 lg:p-8 animate-fade-in">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="mb-10">
                    <h1 className="text-4xl font-bold text-white mb-3 tracking-tight">GATE Preparation</h1>
                    <p className="text-lg text-gray-300">Master your technical skills with practice questions and progress tracking.</p>
                </div>

                {/* Tabs */}
                <div className="mb-10 flex flex-wrap gap-4">
                    {[
                        { id: 'practice', icon: BookOpen, label: 'Practice' },
                        { id: 'progress', icon: BarChart3, label: 'Progress' },
                        { id: 'resources', icon: Library, label: 'Resources' }
                    ].map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center gap-2 px-6 py-3 rounded-2xl font-bold transition-all duration-300 ${activeTab === tab.id
                                ? 'bg-cyan-600 text-white shadow-[0_0_20px_rgba(8,145,178,0.4)] scale-105'
                                : 'bg-slate-800/40 text-gray-400 hover:bg-slate-800/60 hover:text-white border border-white/5'
                                }`}
                        >
                            <tab.icon className="w-5 h-5" />
                            {tab.label}
                        </button>
                    ))}
                </div>

                {/* Practice Tab */}
                {activeTab === 'practice' && questions.length > 0 && (
                    <div className="bg-surface/40 backdrop-blur-md border border-white/10 rounded-3xl overflow-hidden shadow-2xl animate-slide-up">
                        {/* Question Header */}
                        <div className="px-8 py-6 border-b border-white/10 flex items-center justify-between">
                            <div className="flex items-center gap-6">
                                <div className="flex flex-col">
                                    <span className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">Status</span>
                                    <span className="text-white font-bold">
                                        Question {currentQuestion + 1} of {questions.length}
                                    </span>
                                </div>
                                <div className="flex flex-col">
                                    <span className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">Difficulty</span>
                                    <span className={`px-3 py-0.5 rounded-lg text-sm font-bold border ${getDifficultyColor(questions[currentQuestion].difficulty)}`}>
                                        {questions[currentQuestion].difficulty}
                                    </span>
                                </div>
                            </div>
                            <div className="flex items-center gap-3 bg-white/5 px-4 py-2 rounded-2xl border border-white/5">
                                <Award className="w-5 h-5 text-amber-400" />
                                <span className="text-white font-bold">{questions[currentQuestion].marks} Marks</span>
                            </div>
                        </div>

                        <div className="p-8">
                            {/* Subject and Topic */}
                            <div className="flex items-center gap-3 mb-8">
                                <span className="text-sm font-bold text-cyan-400 bg-cyan-400/10 px-3 py-1 rounded-full border border-cyan-400/20">
                                    {questions[currentQuestion].subject}
                                </span>
                                <ChevronRight className="w-4 h-4 text-gray-600" />
                                <span className="text-sm font-medium text-white">{questions[currentQuestion].topic}</span>
                            </div>

                            {/* Question Container */}
                            <div className="mb-10">
                                <div className="text-2xl font-bold text-white mb-8 leading-snug">
                                    {questions[currentQuestion].question}
                                </div>

                                {/* Options */}
                                <div className="grid grid-cols-1 gap-4">
                                    {questions[currentQuestion].options?.map((option, index) => (
                                        <button
                                            key={index}
                                            onClick={() => !showResult && setSelectedAnswer(index)}
                                            disabled={showResult}
                                            className={`group w-full text-left p-5 rounded-2xl border-2 transition-all duration-300 transform ${showResult
                                                ? index === result?.correct_answer
                                                    ? 'border-emerald-500 bg-emerald-500/10'
                                                    : index === selectedAnswer
                                                        ? 'border-rose-500 bg-rose-500/10'
                                                        : 'border-white/5 bg-white/5 opacity-50'
                                                : selectedAnswer === index
                                                    ? 'border-cyan-500 bg-cyan-500/10 scale-[1.01] shadow-[0_0_20px_rgba(6,182,212,0.2)]'
                                                    : 'border-white/5 bg-white/5 hover:border-white/20 hover:bg-white/10'
                                                }`}
                                        >
                                            <div className="flex items-center gap-4">
                                                <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-lg transition-colors ${showResult
                                                    ? index === result?.correct_answer
                                                        ? 'bg-emerald-500 text-white'
                                                        : index === selectedAnswer
                                                            ? 'bg-rose-500 text-white'
                                                            : 'bg-slate-700 text-gray-300'
                                                    : selectedAnswer === index
                                                        ? 'bg-cyan-500 text-white'
                                                        : 'bg-slate-700 text-gray-300 group-hover:bg-slate-600 group-hover:text-white'
                                                    }`}>
                                                    {String.fromCharCode(65 + index)}
                                                </div>
                                                <span className={`text-lg transition-colors ${showResult || selectedAnswer === index ? 'text-white font-medium' : 'text-gray-300'}`}>
                                                    {option}
                                                </span>
                                                {showResult && index === result?.correct_answer && (
                                                    <CheckCircle className="w-6 h-6 text-emerald-500 ml-auto" />
                                                )}
                                                {showResult && index === selectedAnswer && index !== result?.correct_answer && (
                                                    <XCircle className="w-6 h-6 text-rose-500 ml-auto" />
                                                )}
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            </div>

                            {/* Result/Explanation */}
                            {showResult && result && (
                                <div className={`p-6 rounded-3xl mb-8 border backdrop-blur-md animate-fade-in ${result.correct ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-rose-500/10 border-rose-500/30'}`}>
                                    <div className="flex items-center mb-4">
                                        <div className={`p-2 rounded-xl mr-4 ${result.correct ? 'bg-emerald-500/20' : 'bg-rose-500/20'}`}>
                                            {result.correct ? (
                                                <CheckCircle className="w-6 h-6 text-emerald-400" />
                                            ) : (
                                                <XCircle className="w-6 h-6 text-rose-400" />
                                            )}
                                        </div>
                                        <div className="flex flex-col">
                                            <span className={`text-xl font-bold ${result.correct ? 'text-emerald-400' : 'text-rose-400'}`}>
                                                {result.correct ? 'Brilliant Answer!' : 'Not quite right'}
                                            </span>
                                            <span className="text-sm text-gray-400">
                                                Performance: {result.marks_awarded}/{result.total_marks} marks earned
                                            </span>
                                        </div>
                                    </div>
                                    <div className="pl-14">
                                        <p className="text-white text-lg leading-relaxed">{result.explanation}</p>
                                    </div>
                                </div>
                            )}

                            {/* Action Buttons */}
                            <div className="pt-6">
                                {!showResult ? (
                                    <button
                                        onClick={handleSubmitAnswer}
                                        disabled={selectedAnswer === null || loading}
                                        className="w-full py-5 bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold text-xl rounded-2xl shadow-lg transition-all transform active:scale-95"
                                    >
                                        {loading ? <Loader2 className="w-6 h-6 animate-spin mx-auto text-white" /> : "Verify and Submit Answer"}
                                    </button>
                                ) : (
                                    <button
                                        onClick={handleNextQuestion}
                                        disabled={currentQuestion >= questions.length - 1}
                                        className="w-full py-5 bg-slate-700 hover:bg-slate-600 disabled:opacity-30 disabled:cursor-not-allowed text-white font-bold text-xl rounded-2xl shadow-lg transition-all flex items-center justify-center gap-3"
                                    >
                                        Proceed to Next Question <ChevronRight className="w-6 h-6" />
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>
                )}

                {/* Progress Tab */}
                {activeTab === 'progress' && progress && (
                    <div className="space-y-8 animate-slide-up">
                        {/* Overall Stats */}
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                            {[
                                { label: 'Total Attempted', value: progress.total_attempted, color: 'text-white' },
                                { label: 'Correct Answers', value: progress.total_correct, color: 'text-emerald-400' },
                                { label: 'Total Marks', value: progress.total_marks, color: 'text-cyan-400' },
                                { label: 'Overall Accuracy', value: `${progress.accuracy}%`, color: 'text-amber-400' }
                            ].map((stat, i) => (
                                <div key={i} className="bg-surface/40 backdrop-blur-md border border-white/10 p-6 rounded-3xl">
                                    <div className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">{stat.label}</div>
                                    <div className={`text-3xl font-bold ${stat.color}`}>{stat.value}</div>
                                </div>
                            ))}
                        </div>

                        {/* Subject-wise Progress */}
                        <div className="bg-surface/40 backdrop-blur-md border border-white/10 p-8 rounded-3xl shadow-2xl">
                            <h3 className="text-2xl font-bold text-white mb-8 flex items-center gap-3">
                                <TrendingUp className="w-6 h-6 text-cyan-400" />
                                Subject-wise Performance Matrix
                            </h3>
                            <div className="space-y-8">
                                {Object.entries(progress.subject_wise).map(([subject, stats]) => (
                                    <div key={subject} className="group">
                                        <div className="flex items-center justify-between mb-3">
                                            <div className="flex items-center gap-3">
                                                <div className="w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.8)]"></div>
                                                <span className="text-lg font-bold text-white group-hover:text-cyan-400 transition-colors">{subject}</span>
                                            </div>
                                            <span className="text-sm font-medium text-gray-300 bg-white/5 px-3 py-1 rounded-full border border-white/5">
                                                {stats.correct}/{stats.attempted} Correct ({stats.accuracy.toFixed(1)}%)
                                            </span>
                                        </div>
                                        <div className="w-full bg-slate-800 rounded-full h-3 overflow-hidden border border-white/5">
                                            <div
                                                className="bg-gradient-to-r from-cyan-600 to-cyan-400 h-full rounded-full transition-all duration-1000 ease-out shadow-[0_0_10px_rgba(34,211,238,0.3)]"
                                                style={{ width: `${stats.accuracy}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}


                {/* Resources Tab */}
                {activeTab === 'resources' && (
                    <div className="animate-slide-up">
                        {loading && resources.length === 0 ? (
                            <div className="flex items-center justify-center py-20">
                                <Loader2 className="w-10 h-10 text-primary animate-spin" />
                            </div>
                        ) : resources.length === 0 ? (
                            <div className="bg-surface/40 backdrop-blur-md border border-white/10 rounded-3xl p-20 text-center">
                                <p className="text-xl text-gray-400">No preparation resources found yet.</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 gap-10">
                                {resources.map((category, idx) => (
                                    <div key={idx} className="bg-surface/40 backdrop-blur-md border border-white/10 rounded-3xl overflow-hidden shadow-2xl">
                                        <div className="bg-white/5 px-8 py-6 border-b border-white/10">
                                            <h3 className="text-2xl font-bold text-white flex items-center gap-3">
                                                <Library className="w-6 h-6 text-cyan-400" />
                                                {category.subject}
                                            </h3>
                                        </div>
                                        <div className="p-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                                            {category.resources.map((resource, rIdx) => (
                                                <div key={rIdx} className="group bg-white/5 border border-white/5 rounded-2xl p-6 hover:bg-white/10 hover:border-cyan-500/30 transition-all duration-300">
                                                    <div className="flex items-start justify-between">
                                                        <div className="flex-1">
                                                            <h4 className="text-xl font-bold text-white mb-3 group-hover:text-cyan-400 transition-colors">
                                                                {resource.title}
                                                            </h4>
                                                            <div className="flex flex-wrap items-center gap-4 text-sm">
                                                                <span className="flex items-center gap-2 text-gray-400 bg-slate-800/60 px-3 py-1 rounded-xl">
                                                                    {resource.type === 'Video Lectures' ? (
                                                                        <Video className="w-4 h-4 text-rose-400" />
                                                                    ) : (
                                                                        <FileText className="w-4 h-4 text-cyan-400" />
                                                                    )}
                                                                    {resource.type}
                                                                </span>
                                                                <span className="text-gray-600">•</span>
                                                                <span className="text-gray-300 font-medium">{resource.provider}</span>
                                                            </div>
                                                        </div>
                                                        <a
                                                            href={resource.url}
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                            className="w-12 h-12 flex items-center justify-center rounded-2xl bg-cyan-600 hover:bg-cyan-500 text-white shadow-lg transition-all transform hover:scale-110 active:scale-90"
                                                            title="Launch Resource"
                                                        >
                                                            <ExternalLink className="w-6 h-6" />
                                                        </a>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default GATEPrep;

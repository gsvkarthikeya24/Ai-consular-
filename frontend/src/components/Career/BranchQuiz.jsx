import { useState, useEffect } from 'react';
import { Brain, ArrowRight, ArrowLeft, Loader2, Sparkles, CheckCircle, Info, Bot } from 'lucide-react';
import api from '../../utils/api';
import Card from '../UI/Card';
import Button from '../shared/Button';
import Section from '../UI/Section';
import Navbar from '../shared/Navbar';

const BranchQuiz = () => {
    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [currentStep, setCurrentStep] = useState(0);
    const [answers, setAnswers] = useState({});
    const [result, setResult] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchQuestions();
    }, []);

    const fetchQuestions = async () => {
        setLoading(true);
        try {
            const response = await api.get('/api/quiz/questions');
            setQuestions(response.data);
        } catch (err) {
            setError('Failed to load quiz questions. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleOptionSelect = (questionId, optionId) => {
        setAnswers(prev => ({
            ...prev,
            [questionId]: optionId
        }));
    };

    const handleNext = () => {
        if (currentStep < questions.length - 1) {
            setCurrentStep(prev => prev + 1);
        }
    };

    const handleBack = () => {
        if (currentStep > 0) {
            setCurrentStep(prev => prev - 1);
        }
    };

    const handleSubmit = async () => {
        setSubmitting(true);
        setError('');
        try {
            const formattedAnswers = Object.entries(answers).map(([qId, optId]) => ({
                question_id: qId,
                option_id: optId
            }));

            const response = await api.post('/api/quiz/recommend', formattedAnswers);
            setResult(response.data);
        } catch (err) {
            setError('Failed to get recommendations. Please ensure you answered all questions.');
            console.error(err);
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-background">
                <Navbar />
                <div className="flex flex-col items-center justify-center py-32">
                    <Loader2 className="w-12 h-12 text-primary animate-spin mb-4" />
                    <p className="text-white text-lg">Loading your path to success...</p>
                </div>
            </div>
        );
    }

    if (result) {
        return (
            <div className="min-h-screen bg-background pb-20">
                <Navbar />
                <div className="pt-24 max-w-4xl mx-auto px-4">
                    <div className="text-center mb-12 animate-fade-in">
                        <div className="inline-flex p-4 rounded-full bg-green-500/10 border border-green-500/20 mb-6">
                            <CheckCircle className="w-12 h-12 text-green-400" />
                        </div>
                        <h1 className="text-4xl font-bold text-white mb-4">Your Engineering Match</h1>
                        <p className="text-text-secondary text-lg">Based on your unique profile and preferences.</p>
                    </div>

                    <Card className="p-8 border-primary/30 bg-surface-light/40 backdrop-blur-md mb-8 animate-slide-up">
                        <div className="flex flex-col md:flex-row gap-8 items-center">
                            <div className="w-24 h-24 bg-primary/20 rounded-2xl flex items-center justify-center border border-primary/30 shrink-0">
                                <Brain className="w-12 h-12 text-primary-glow" />
                            </div>
                            <div>
                                <h2 className="text-3xl font-bold text-primary-glow mb-3">{result.recommended_branch}</h2>
                                <p className="text-white text-lg leading-relaxed">{result.description}</p>
                            </div>
                        </div>

                        <div className="mt-8 pt-8 border-t border-white/10">
                            <h3 className="text-lg font-bold text-white mb-4">Why this branch?</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {Object.entries(result.scores).map(([branch, score]) => (
                                    <div key={branch} className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/5">
                                        <span className="text-gray-300 font-medium">{branch} Compatibility</span>
                                        <div className="flex items-center gap-2">
                                            <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden">
                                                <div
                                                    className={`h-full ${branch === result.recommended_branch ? 'bg-primary-500' : 'bg-gray-500'}`}
                                                    style={{ width: `${(score / 30) * 100}%` }}
                                                ></div>
                                            </div>
                                            <span className="text-xs text-white font-bold">{score} pts</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </Card>

                    <div className="flex justify-center gap-4">
                        <Button onClick={() => window.location.href = '/career'} variant="secondary">Back to Counselor</Button>
                        <Button onClick={() => window.location.href = '/courses'} className="shadow-[0_0_20px_rgba(6,182,212,0.3)]">Explore Courses</Button>
                    </div>
                </div>
            </div>
        );
    }

    const currentQuestion = questions[currentStep];
    const progress = ((currentStep + 1) / questions.length) * 100;

    return (
        <div className="min-h-screen bg-background pb-20">
            <Navbar />

            <div className="pt-24 max-w-6xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Quiz Area */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="flex justify-between items-end mb-2">
                        <h2 className="text-text-secondary font-bold uppercase tracking-wider text-xs">Question {currentStep + 1} of {questions.length}</h2>
                        <span className="text-primary-glow font-bold text-sm">{Math.round(progress)}% Complete</span>
                    </div>
                    <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden mb-8 border border-white/5">
                        <div
                            className="h-full bg-primary-500 transition-all duration-500 shadow-[0_0_10px_rgba(6,182,212,0.5)]"
                            style={{ width: `${progress}%` }}
                        ></div>
                    </div>

                    <Card className="p-8 border-white/10 bg-surface/60 backdrop-blur-sm shadow-xl min-h-[400px] flex flex-col">
                        <h3 className="text-2xl font-bold text-white mb-8 leading-tight">
                            {currentQuestion.question}
                        </h3>

                        <div className="space-y-4 flex-grow">
                            {currentQuestion.options.map((option) => (
                                <button
                                    key={option.id}
                                    onClick={() => handleOptionSelect(currentQuestion.id, option.id)}
                                    className={`w-full text-left p-5 rounded-2xl border transition-all flex items-center gap-4 group ${answers[currentQuestion.id] === option.id
                                            ? 'bg-primary/20 border-primary-500 shadow-[0_0_15px_rgba(6,182,212,0.2)]'
                                            : 'bg-white/5 border-white/10 hover:border-white/20 hover:bg-white/10'
                                        }`}
                                >
                                    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center shrink-0 ${answers[currentQuestion.id] === option.id
                                            ? 'border-primary-500 bg-primary-500'
                                            : 'border-white/20'
                                        }`}>
                                        {answers[currentQuestion.id] === option.id && <div className="w-2 h-2 bg-white rounded-full"></div>}
                                    </div>
                                    <span className={`text-lg transition-colors ${answers[currentQuestion.id] === option.id ? 'text-white font-bold' : 'text-gray-300 group-hover:text-white'
                                        }`}>
                                        {option.text}
                                    </span>
                                </button>
                            ))}
                        </div>

                        <div className="flex justify-between items-center mt-12 pt-6 border-t border-white/5">
                            <Button
                                onClick={handleBack}
                                variant="ghost"
                                disabled={currentStep === 0}
                                className="flex items-center gap-2"
                            >
                                <ArrowLeft className="w-4 h-4" /> Back
                            </Button>

                            {currentStep === questions.length - 1 ? (
                                <Button
                                    onClick={handleSubmit}
                                    loading={submitting}
                                    disabled={!answers[currentQuestion.id]}
                                    className="px-10 shadow-[0_0_20px_rgba(6,182,212,0.3)]"
                                >
                                    Predict My Branch
                                </Button>
                            ) : (
                                <Button
                                    onClick={handleNext}
                                    disabled={!answers[currentQuestion.id]}
                                    className="flex items-center gap-2 group"
                                >
                                    Next Question <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                                </Button>
                            )}
                        </div>
                    </Card>

                    {error && (
                        <p className="text-red-400 text-center text-sm font-medium animate-pulse">{error}</p>
                    )}
                </div>

                {/* AI Mentor Sidebar */}
                <div className="space-y-6">
                    <Card className="bg-gradient-to-br from-primary-900/40 to-surface border-primary/20 p-6 shadow-2xl relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-4 opacity-10">
                            <Bot className="w-20 h-20 text-primary-glow" />
                        </div>
                        <div className="relative z-10">
                            <div className="flex items-center gap-3 mb-6">
                                <div className="p-2 bg-primary/20 rounded-lg">
                                    <Bot className="w-6 h-6 text-primary-glow" />
                                </div>
                                <h3 className="font-bold text-white text-lg">Mentor Guidance</h3>
                            </div>

                            <div className="space-y-4">
                                <div className="p-4 bg-primary/10 rounded-xl border border-primary/20 backdrop-blur-sm animate-fade-in shadow-inner" key={currentStep}>
                                    <p className="text-primary-100 text-sm italic leading-relaxed font-medium">
                                        "{currentQuestion.mentor_guidance}"
                                    </p>
                                </div>

                                <div className="flex items-start gap-3 p-4 bg-white/5 rounded-xl border border-white/5">
                                    <Info className="w-5 h-5 text-primary-400 shrink-0 mt-0.5" />
                                    <div>
                                        <h4 className="text-xs font-bold text-text-muted uppercase mb-1">Did you know?</h4>
                                        <p className="text-xs text-text-secondary leading-relaxed">
                                            Most engineering students find their true passion after the first year. This quiz helps you start on the right foot!
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </Card>

                    <div className="p-6 bg-surface-light/30 rounded-3xl border border-white/5 text-center">
                        <Sparkles className="w-8 h-8 text-yellow-400 mx-auto mb-3" />
                        <h4 className="text-white font-bold mb-1">Analyze Your Future</h4>
                        <p className="text-text-secondary text-xs">Our AI analyzes data from 5000+ career trajectories to match you.</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BranchQuiz;

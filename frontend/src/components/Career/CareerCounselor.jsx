import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Compass, Target, Brain, ArrowRight, Loader2, Star, ChevronRight } from 'lucide-react';
import api from '../../utils/api';
import Card from '../UI/Card';
import Button from '../shared/Button';
import Section from '../UI/Section';
import RoadmapModal from './RoadmapModal';

const CareerCounselor = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [roadmapLoading, setRoadmapLoading] = useState(false);
    const [recommendations, setRecommendations] = useState(null);
    const [selectedRoadmap, setSelectedRoadmap] = useState(null);
    const [error, setError] = useState('');

    const fetchRecommendations = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await api.post('/api/career/recommend/detailed');
            setRecommendations(response.data.recommended_domains.matches || []);
        } catch (err) {
            setError('Failed to get personal recommendations. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleViewRoadmap = async (domainId) => {
        setRoadmapLoading(true);
        try {
            const response = await api.get(`/api/career/roadmap/${domainId}`);
            setSelectedRoadmap(response.data);
        } catch (err) {
            console.error('Failed to fetch roadmap:', err);
            setError('Failed to load roadmap details. Please try again.');
        } finally {
            setRoadmapLoading(false);
        }
    };

    return (
        <div className="max-w-7xl mx-auto">
            <Section className="!py-0">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6">
                    <div className="max-w-2xl">
                        <h1 className="text-4xl font-heading font-bold text-white mb-3 tracking-tight">
                            AI Career Counselor
                        </h1>
                        <p className="text-lg text-text-secondary leading-relaxed">
                            Personalized career path recommendations based on your branch, interests, and academic performance.
                        </p>
                    </div>
                    {!recommendations && (
                        <Button onClick={fetchRecommendations} loading={loading} size="lg" className="shadow-[0_0_20px_rgba(6,182,212,0.3)]">
                            {loading ? "Analyzing Profile..." : "Get AI Insights"}
                        </Button>
                    )}
                </div>

                {error && (
                    <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 mb-8 backdrop-blur-sm">
                        {error}
                    </div>
                )}

                {!recommendations && !loading && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
                        <div className="relative overflow-hidden text-center py-16 bg-surface/30 rounded-3xl border border-white/5 backdrop-blur-sm">
                            <div className="absolute inset-0 bg-gradient-to-b from-primary/5 to-transparent opacity-50" />
                            <div className="relative z-10">
                                <div className="w-16 h-16 bg-surface-light rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl border border-white/5">
                                    <Compass className="w-8 h-8 text-primary-glow animate-pulse-slow" />
                                </div>
                                <h3 className="text-xl font-bold text-white mb-3">Explore Your Future</h3>
                                <p className="text-text-secondary max-w-xs mx-auto mb-8 text-sm">
                                    Analyze your student profile and market trends for career paths.
                                </p>
                                <Button onClick={fetchRecommendations} size="md" className="px-8 shadow-[0_0_20px_rgba(6,182,212,0.3)]">
                                    Start Analysis
                                </Button>
                            </div>
                        </div>

                        <div className="relative overflow-hidden text-center py-16 bg-gradient-to-br from-primary-900/20 to-surface/30 rounded-3xl border border-primary/20 backdrop-blur-sm">
                            <div className="absolute inset-0 bg-primary/5 opacity-50" />
                            <div className="relative z-10">
                                <div className="w-16 h-16 bg-primary/20 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl border border-primary/20">
                                    <Brain className="w-8 h-8 text-primary-glow" />
                                </div>
                                <h3 className="text-xl font-bold text-white mb-3">Branch Selection Quiz</h3>
                                <p className="text-text-secondary max-w-xs mx-auto mb-8 text-sm">
                                    Not sure which branch to pick? Take our 10-question expert quiz.
                                </p>
                                <Button onClick={() => navigate('/branch-quiz')} variant="secondary" size="md" className="px-8">
                                    Take the Quiz
                                </Button>
                            </div>
                        </div>
                    </div>
                )}

                {loading && (
                    <div className="flex flex-col items-center justify-center py-32">
                        <div className="relative">
                            <div className="absolute inset-0 bg-primary-glow blur-xl opacity-20 animate-pulse"></div>
                            <Loader2 className="relative w-16 h-16 text-primary animate-spin mb-6" />
                        </div>
                        <p className="text-xl font-medium text-white">Analyzing your profile...</p>
                        <p className="text-text-secondary mt-2">Connecting to AI Consular engine</p>
                    </div>
                )}

                {recommendations && (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in pb-12">
                        {recommendations.map((path, index) => (
                            <Card key={index} className="flex flex-col h-full group hover:bg-surface-light/40 transition-colors">
                                <div className="flex justify-between items-start mb-6">
                                    <div className="p-3 bg-primary/10 rounded-xl border border-primary/20 group-hover:bg-primary/20 transition-colors">
                                        <Target className="w-6 h-6 text-primary-glow" />
                                    </div>
                                    <div className="flex items-center gap-1.5 bg-green-500/10 text-green-400 px-3 py-1 rounded-full text-xs font-bold border border-green-500/20 shadow-[0_0_10px_rgba(74,222,128,0.2)]">
                                        <Star className="w-3.5 h-3.5 fill-current" />
                                        {path.match_score}% Match
                                    </div>
                                </div>

                                <h3 className="text-2xl font-bold text-white mb-3 group-hover:text-primary-glow transition-colors">
                                    {path.domain_title}
                                </h3>

                                <p className="text-text-secondary text-sm mb-8 flex-grow leading-relaxed">
                                    {path.reasoning}
                                </p>

                                <div className="mt-auto space-y-5">
                                    <div className="p-4 bg-surface-light/50 rounded-xl border border-white/5">
                                        <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-2">Recommended Next Step</p>
                                        <p className="text-sm text-text-primary font-medium">{path.next_step}</p>
                                    </div>

                                    <button
                                        onClick={() => handleViewRoadmap(path.domain_id)}
                                        disabled={roadmapLoading}
                                        className="w-full flex items-center justify-center gap-2 text-primary-glow font-semibold hover:text-white py-3 border-t border-white/5 mt-2 text-sm transition-colors group/btn disabled:opacity-50"
                                    >
                                        {roadmapLoading ? (
                                            <Loader2 className="w-4 h-4 animate-spin" />
                                        ) : (
                                            <>
                                                View Detailed Roadmap <ChevronRight className="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" />
                                            </>
                                        )}
                                    </button>
                                </div>
                            </Card>
                        ))}

                        <Card
                            onClick={() => navigate('/mentor')}
                            className="flex flex-col items-center justify-center text-center p-8 bg-gradient-to-br from-primary-dark to-primary-900 border-primary/30 shadow-[0_0_30px_rgba(8,145,178,0.15)] cursor-pointer group hover:scale-[1.02] transition-transform"
                        >
                            <div className="w-16 h-16 bg-white/10 rounded-full flex items-center justify-center mb-6 group-hover:bg-white/20 transition-colors backdrop-blur-sm">
                                <Brain className="w-8 h-8 text-white" />
                            </div>
                            <h3 className="text-2xl font-bold text-white mb-3">Need More Clarity?</h3>
                            <p className="text-primary-100 text-sm mb-8 leading-relaxed">
                                Schedule a deep-dive session with our AI Mentor or refine your interests to get better recommendations.
                            </p>
                            <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center border border-white/20 group-hover:bg-white/20 transition-colors">
                                <ArrowRight className="w-6 h-6 text-white" />
                            </div>
                        </Card>
                    </div>
                )}
            </Section>

            <RoadmapModal
                isOpen={!!selectedRoadmap}
                onClose={() => setSelectedRoadmap(null)}
                roadmapData={selectedRoadmap}
            />
        </div>
    );
};

export default CareerCounselor;

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    BookOpen,
    Compass,
    FileText,
    Briefcase,
    TrendingUp,
    Award,
    Target,
    Brain,
    GraduationCap
} from 'lucide-react';
import Navbar from '../shared/Navbar';
import Card from '../UI/Card';
import Section from '../UI/Section';
import Loader from '../shared/Loader';
import api from '../../utils/api';
import { getUser } from '../../utils/auth';

const StudentDashboard = () => {
    const user = getUser();
    const navigate = useNavigate();
    const [stats, setStats] = useState({
        tasks_completed: 0,
        courses_recommended: 0,
        internships_tracked: 0,
        career_readiness: 0
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            setLoading(true);
            try {
                const response = await api.get('/api/stats/student');
                setStats(response.data);
            } catch (err) {
                console.error("Failed to fetch dashboard stats", err);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    if (loading) {
        return (
            <>
                <Navbar />
                <Loader text="Loading your dashboard..." />
            </>
        );
    }

    return (
        <div className="min-h-screen pb-20">
            <Navbar />

            <div className="pt-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Welcome Section */}
                <div className="mb-12 animate-fade-in relative z-10 flex justify-between items-start">
                    <div>
                        <h1 className="text-4xl md:text-5xl font-heading font-bold text-white mb-2 drop-shadow-lg tracking-tight">
                            Welcome back, <span className="bg-gradient-to-r from-primary-glow to-secondary-glow bg-clip-text text-transparent">{user?.name}</span>! 👋
                        </h1>
                        <p className="text-xl text-text-secondary font-light">
                            {user?.branch} Engineering • Year {user?.year} • <span className="text-primary-glow font-medium">{user?.career_goal}</span>
                        </p>
                    </div>
                    <div className="flex flex-col items-end">
                        <span className={`px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest border ${user?.status === 'active' ? 'bg-green-500/10 text-green-400 border-green-500/20' : 'bg-slate-500/10 text-slate-400 border-slate-500/20'
                            }`}>
                            {user?.status || 'Active'}
                        </span>
                        <p className="text-[10px] text-text-muted mt-2 font-bold uppercase tracking-tighter">
                            Logins: {user?.login_count || stats.tasks_completed + 1}
                        </p>
                    </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12 animate-slide-up">
                    <Card onClick={() => navigate('/analytics')} className="cursor-pointer bg-surface/40 hover:bg-surface/60 transition-all hover:scale-[1.02] border-primary/20 group">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-text-muted mb-1 font-medium uppercase tracking-wider group-hover:text-primary transition-colors">Tasks Completed</p>
                                <p className="text-4xl font-bold text-white font-heading">{stats.tasks_completed}</p>
                            </div>
                            <div className="p-3 bg-primary/10 rounded-xl border border-primary/20 shadow-[0_0_15px_rgba(6,182,212,0.15)] group-hover:shadow-primary/30 transition-shadow">
                                <BookOpen className="w-8 h-8 text-primary" />
                            </div>
                        </div>
                    </Card>

                    <Card className="bg-surface/40 border-secondary/20 hover:scale-[1.02] transition-transform group">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-text-muted mb-1 font-medium uppercase tracking-wider group-hover:text-secondary transition-colors">Courses</p>
                                <p className="text-4xl font-bold text-white font-heading">{stats.courses_recommended}</p>
                            </div>
                            <div className="p-3 bg-secondary/10 rounded-xl border border-secondary/20 shadow-[0_0_15px_rgba(168,85,247,0.15)] group-hover:shadow-secondary/30 transition-shadow">
                                <Award className="w-8 h-8 text-secondary" />
                            </div>
                        </div>
                    </Card>

                    <Card className="bg-surface/40 border-pink-500/20 hover:scale-[1.02] transition-transform group">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-text-muted mb-1 font-medium uppercase tracking-wider group-hover:text-pink-400 transition-colors">Internships</p>
                                <p className="text-4xl font-bold text-white font-heading">{stats.internships_tracked}</p>
                            </div>
                            <div className="p-3 bg-pink-500/10 rounded-xl border border-pink-500/20 shadow-[0_0_15_rgba(236,72,153,0.15)] group-hover:shadow-pink-500/30 transition-shadow">
                                <Briefcase className="w-8 h-8 text-pink-500" />
                            </div>
                        </div>
                    </Card>

                    <Card onClick={() => navigate('/analytics')} className="cursor-pointer bg-surface/40 border-orange-500/20 hover:scale-[1.02] transition-transform group">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-text-muted mb-1 font-medium uppercase tracking-wider group-hover:text-orange-400 transition-colors">Readiness</p>
                                <p className="text-4xl font-bold text-white font-heading">{stats.career_readiness}%</p>
                            </div>
                            <div className="p-3 bg-orange-500/10 rounded-xl border border-orange-500/20 shadow-[0_0_15_rgba(249,115,22,0.15)] group-hover:shadow-orange-500/30 transition-shadow">
                                <TrendingUp className="w-8 h-8 text-orange-500" />
                            </div>
                        </div>
                    </Card>
                </div>

                {/* Quick Actions */}
                <Section title="Quick Actions" subtitle="Everything you need to succeed in your career journey" className="!py-0">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <Card onClick={() => navigate('/career')} className="cursor-pointer group hover:bg-surface-light/60 transition-colors">
                            <div className="flex items-start space-x-4">
                                <div className="p-3 bg-primary/10 rounded-xl group-hover:bg-primary/20 transition-colors">
                                    <Compass className="w-6 h-6 text-primary-glow" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-white text-lg mb-1 group-hover:text-primary-glow transition-colors">Career Guidance</h3>
                                    <p className="text-sm text-text-secondary leading-relaxed">
                                        Personalized career path recommendations based on your profile
                                    </p>
                                </div>
                            </div>
                        </Card>

                        <Card onClick={() => navigate('/resume')} className="cursor-pointer group hover:bg-surface-light/60 transition-colors">
                            <div className="flex items-start space-x-4">
                                <div className="p-3 bg-secondary/10 rounded-xl group-hover:bg-secondary/20 transition-colors">
                                    <FileText className="w-6 h-6 text-secondary-glow" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-white text-lg mb-1 group-hover:text-secondary-glow transition-colors">Resume Builder</h3>
                                    <p className="text-sm text-text-secondary leading-relaxed">
                                        Create ATS-optimized resumes with AI-generated content
                                    </p>
                                </div>
                            </div>
                        </Card>

                        <Card onClick={() => navigate('/mentor')} className="cursor-pointer group hover:bg-surface-light/60 transition-colors">
                            <div className="flex items-start space-x-4">
                                <div className="p-3 bg-green-500/10 rounded-xl group-hover:bg-green-500/20 transition-colors">
                                    <Brain className="w-6 h-6 text-green-400" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-white text-lg mb-1 group-hover:text-green-400 transition-colors">AI Mentor Chat</h3>
                                    <p className="text-sm text-text-secondary leading-relaxed">
                                        Get academic help, motivation, and productivity tips
                                    </p>
                                </div>
                            </div>
                        </Card>

                        <Card onClick={() => navigate('/interview')} className="cursor-pointer group hover:bg-surface-light/60 transition-colors">
                            <div className="flex items-start space-x-4">
                                <div className="p-3 bg-indigo-500/10 rounded-xl group-hover:bg-indigo-500/20 transition-colors">
                                    <Target className="w-6 h-6 text-indigo-400" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-white text-lg mb-1 group-hover:text-indigo-400 transition-colors">Interview Prep</h3>
                                    <p className="text-sm text-text-secondary leading-relaxed">
                                        Master your technical and behavioral interviews
                                    </p>
                                </div>
                            </div>
                        </Card>

                        <Card onClick={() => navigate('/internships')} className="cursor-pointer group hover:bg-surface-light/60 transition-colors">
                            <div className="flex items-start space-x-4">
                                <div className="p-3 bg-yellow-500/10 rounded-xl group-hover:bg-yellow-500/20 transition-colors">
                                    <Briefcase className="w-6 h-6 text-yellow-500" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-white text-lg mb-1 group-hover:text-yellow-500 transition-colors">Internships</h3>
                                    <p className="text-sm text-text-secondary leading-relaxed">
                                        Apply and track internship applications
                                    </p>
                                </div>
                            </div>
                        </Card>

                        <Card onClick={() => navigate('/tasks')} className="cursor-pointer group hover:bg-surface-light/60 transition-colors">
                            <div className="flex items-start space-x-4">
                                <div className="p-3 bg-pink-500/10 rounded-xl group-hover:bg-pink-500/20 transition-colors">
                                    <BookOpen className="w-6 h-6 text-pink-500" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-white text-lg mb-1 group-hover:text-pink-500 transition-colors">Tasks & Focus</h3>
                                    <p className="text-sm text-text-secondary leading-relaxed">
                                        Track assignments and get help with deadlines
                                    </p>
                                </div>
                            </div>
                        </Card>

                        <Card onClick={() => navigate('/branch-quiz')} className="cursor-pointer group hover:bg-surface-light/60 transition-colors border-purple-500/20">
                            <div className="flex items-start space-x-4">
                                <div className="p-3 bg-purple-500/10 rounded-xl group-hover:bg-purple-500/20 transition-colors">
                                    <Brain className="w-6 h-6 text-purple-400" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-white text-lg mb-1 group-hover:text-purple-400 transition-colors">Branch Choice Quiz</h3>
                                    <p className="text-sm text-text-secondary leading-relaxed">
                                        Discover your ideal engineering major with our AI predictor
                                    </p>
                                </div>
                            </div>
                        </Card>

                        <Card onClick={() => navigate('/gate')} className="cursor-pointer group hover:bg-surface-light/60 transition-colors border-cyan-500/20">
                            <div className="flex items-start space-x-4">
                                <div className="p-3 bg-cyan-500/10 rounded-xl group-hover:bg-cyan-500/20 transition-colors">
                                    <GraduationCap className="w-6 h-6 text-cyan-400" />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-white text-lg mb-1 group-hover:text-cyan-400 transition-colors">GATE Preparation</h3>
                                    <p className="text-sm text-text-secondary leading-relaxed">
                                        Master technical concepts with practice tests and analytics
                                    </p>
                                </div>
                            </div>
                        </Card>

                    </div>
                </Section>
            </div>
        </div>
    );
};

export default StudentDashboard;

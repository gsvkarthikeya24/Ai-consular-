import React from 'react';
import { useNavigate } from 'react-router-dom';
import { X, Calendar, Target, Award, CheckCircle2, ChevronRight } from 'lucide-react';
import Card from '../UI/Card';

const RoadmapModal = ({ isOpen, onClose, roadmapData }) => {
    const navigate = useNavigate();
    if (!isOpen || !roadmapData) return null;

    const { domain, roadmap_phases, key_skills, certifications, estimated_duration } = roadmapData;

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
            <div className="bg-surface-dark border border-white/10 rounded-3xl w-full max-w-4xl max-h-[90vh] overflow-hidden shadow-2xl animate-slide-up">
                {/* Header */}
                <div className="relative px-8 py-8 border-b border-white/5">
                    <div className="absolute top-0 right-0 p-6">
                        <button
                            onClick={onClose}
                            className="p-2 rounded-xl bg-white/5 hover:bg-white/10 text-white transition-colors group"
                        >
                            <X className="w-5 h-5 group-hover:rotate-90 transition-transform duration-300" />
                        </button>
                    </div>

                    <div className="flex flex-col gap-2">
                        <span className="text-primary-glow font-bold tracking-widest uppercase text-xs">Learning Roadmap</span>
                        <h2 className="text-3xl font-bold text-white tracking-tight">{domain}</h2>
                        <div className="flex items-center gap-4 mt-2">
                            <div className="flex items-center gap-2 text-text-secondary text-sm bg-white/5 px-3 py-1 rounded-full border border-white/5">
                                <Calendar className="w-4 h-4 text-cyan-400" />
                                <span>Total Duration: {estimated_duration} months</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Content */}
                <div className="px-8 py-8 overflow-y-auto max-h-[calc(90vh-160px)] custom-scrollbar">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        {/* Main Timeline */}
                        <div className="lg:col-span-2 space-y-8">
                            <h3 className="text-xl font-bold text-white flex items-center gap-2">
                                <Target className="w-5 h-5 text-primary-glow" />
                                Strategic Phases
                            </h3>

                            <div className="space-y-6 relative before:absolute before:left-[17px] before:top-2 before:bottom-2 before:w-0.5 before:bg-gradient-to-b before:from-primary-glow before:via-primary/20 before:to-transparent">
                                {roadmap_phases.map((phase, idx) => (
                                    <div key={idx} className="relative pl-12 group">
                                        <div className="absolute left-0 top-1 w-9 h-9 bg-surface-dark border-2 border-primary-glow rounded-full flex items-center justify-center z-10 shadow-[0_0_15px_rgba(6,182,212,0.3)] group-hover:scale-110 transition-transform">
                                            <span className="text-xs font-bold text-white">{idx + 1}</span>
                                        </div>
                                        <div className="p-6 bg-white/5 border border-white/5 rounded-2xl hover:border-primary/30 transition-all duration-300">
                                            <div className="flex justify-between items-start mb-3">
                                                <h4 className="text-lg font-bold text-white group-hover:text-primary-glow transition-colors">{phase.phase}</h4>
                                                <span className="text-xs font-medium text-cyan-400 bg-cyan-400/10 px-2 py-0.5 rounded-md border border-cyan-400/20">
                                                    {phase.duration}
                                                </span>
                                            </div>
                                            <p className="text-text-secondary text-sm leading-relaxed">
                                                {phase.focus}
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Sidebar */}
                        <div className="space-y-8">
                            {/* Skills */}
                            <div className="space-y-4">
                                <h3 className="text-lg font-bold text-white border-b border-white/5 pb-2">Key Skills</h3>
                                <div className="flex flex-wrap gap-2">
                                    {key_skills.map((skill, idx) => (
                                        <span key={idx} className="px-3 py-1.5 bg-surface-light border border-white/5 rounded-lg text-xs font-medium text-text-primary hover:border-primary/40 transition-colors">
                                            {skill.name}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            {/* Certifications */}
                            <div className="space-y-4">
                                <h3 className="text-lg font-bold text-white border-b border-white/5 pb-2">Certifications</h3>
                                <div className="space-y-3">
                                    {certifications.map((cert, idx) => (
                                        <div key={idx} className="flex items-center gap-3 p-3 bg-white/5 rounded-xl border border-white/5 hover:border-yellow-500/30 transition-all group">
                                            <Award className="w-5 h-5 text-yellow-500 group-hover:scale-110 transition-transform" />
                                            <span className="text-xs text-text-secondary font-medium">{cert}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Mentorship Link */}
                            <div className="p-5 bg-gradient-to-br from-primary-900/40 to-cyan-900/40 border border-primary/20 rounded-2xl">
                                <h4 className="font-bold text-white text-sm mb-2">Need Help?</h4>
                                <p className="text-xs text-text-secondary mb-4 leading-relaxed">
                                    Get personalized guidance from our AI Mentor for this path.
                                </p>
                                <button
                                    onClick={() => {
                                        navigate('/mentor');
                                        onClose();
                                    }}
                                    className="w-full py-2 bg-primary/20 hover:bg-primary/30 border border-primary/40 rounded-lg text-primary-glow text-xs font-bold flex items-center justify-center gap-2 transition-all"
                                >
                                    Chat with Mentor <ChevronRight className="w-3 h-3" />
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RoadmapModal;

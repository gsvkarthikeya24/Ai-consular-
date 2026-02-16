import { useState, useEffect } from 'react';
import { Briefcase, Plus, Search, Trash2, Edit3, Sparkles, Building2, MapPin, Calendar, Clock, Loader2, X } from 'lucide-react';
import api from '../../utils/api';
import Card from '../shared/Card';
import Button from '../shared/Button';
import Loader from '../shared/Loader';

const InternshipTracker = () => {
    const [internships, setInternships] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [selectedInternship, setSelectedInternship] = useState(null);
    const [formData, setFormData] = useState({
        company: '',
        role: '',
        domain: '',
        status: 'applied',
        notes: ''
    });
    const [aiReview, setAiReview] = useState(null);
    const [aiLoadingId, setAiLoadingId] = useState(null);

    useEffect(() => {
        fetchInternships();
    }, []);

    const fetchInternships = async () => {
        setLoading(true);
        try {
            const response = await api.get('/api/internships');
            setInternships(response.data);
        } catch (err) {
            console.error("Failed to fetch internships", err);
        } finally {
            setLoading(false);
        }
    };

    const handleGetAiReview = async (id) => {
        setAiLoadingId(id);
        try {
            const response = await api.post(`/api/internships/${id}/review`);
            setAiReview(response.data);
            fetchInternships(); // Refresh to get the stored review if any
        } catch (err) {
            console.error("Failed to get AI review", err);
        } finally {
            setAiLoadingId(null);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (isEditing) {
                await api.put(`/api/internships/${selectedInternship._id}`, formData);
            } else {
                await api.post('/api/internships', formData);
            }
            setShowModal(false);
            fetchInternships();
            resetForm();
        } catch (err) {
            console.error("Failed to save internship", err);
        }
    };

    const deleteInternship = async (id) => {
        if (!window.confirm("Are you sure you want to delete this application?")) return;
        try {
            await api.delete(`/api/internships/${id}`);
            fetchInternships();
        } catch (err) {
            console.error("Failed to delete internship", err);
        }
    };

    const resetForm = () => {
        setFormData({ company: '', role: '', domain: '', status: 'applied', notes: '' });
        setIsEditing(false);
        setSelectedInternship(null);
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'offered': return 'bg-green-100 text-green-700';
            case 'interviewing': return 'bg-blue-100 text-blue-700';
            case 'rejected': return 'bg-red-100 text-red-700';
            default: return 'bg-gray-100 text-gray-700';
        }
    };

    if (loading) return <Loader text="Loading your applications..." />;

    return (
        <div className="max-w-6xl mx-auto py-8 px-4">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-2">Internship Tracker</h1>
                    <p className="text-gray-400">Keep track of your applications and get AI-powered improvement suggestions.</p>
                </div>
                <Button onClick={() => { resetForm(); setShowModal(true); }} className="flex items-center gap-2">
                    <Plus className="w-5 h-5" /> Add Application
                </Button>
            </div>

            <div className="grid grid-cols-1 gap-6">
                {internships.length > 0 ? (
                    internships.map((internship) => (
                        <div key={internship._id} className="bg-white border border-gray-200 rounded-3xl p-6 hover:shadow-lg transition-all animate-fade-in group">
                            <div className="flex flex-col md:flex-row justify-between gap-6">
                                <div className="flex-grow">
                                    <div className="flex items-center gap-3 mb-3">
                                        <div className="p-3 bg-primary-50 text-primary-600 rounded-2xl">
                                            <Building2 className="w-6 h-6" />
                                        </div>
                                        <div>
                                            <h3 className="text-xl font-extrabold text-gray-900">{internship.company}</h3>
                                            <p className="text-gray-500 font-medium">{internship.role} • {internship.domain}</p>
                                        </div>
                                    </div>

                                    <div className="flex flex-wrap gap-4 text-sm text-gray-500 mb-4">
                                        <div className="flex items-center gap-1.5 bg-gray-50 px-3 py-1.5 rounded-full">
                                            <Calendar className="w-4 h-4" />
                                            Applied {new Date(internship.applied_date).toLocaleDateString()}
                                        </div>
                                        <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full font-bold uppercase text-[10px] tracking-wider ${getStatusColor(internship.status)}`}>
                                            <Clock className="w-4 h-4" />
                                            {internship.status}
                                        </div>
                                    </div>

                                    {internship.notes && (
                                        <p className="text-sm text-gray-600 italic bg-gray-50 p-4 rounded-2xl border border-gray-100 mb-4">
                                            "{internship.notes}"
                                        </p>
                                    )}

                                    {internship.ai_review && (
                                        <div className="mb-4 bg-emerald-50 border border-emerald-100 p-4 rounded-2xl">
                                            <div className="flex items-center gap-2 text-emerald-700 font-bold text-xs uppercase tracking-wider mb-2">
                                                <Sparkles className="w-4 h-4" /> AI Mentor Feedback
                                            </div>
                                            <p className="text-sm text-emerald-800 leading-relaxed">
                                                {internship.ai_review}
                                            </p>
                                        </div>
                                    )}

                                    {/* AI review button */}
                                    <div className="flex items-center gap-2">
                                        <button
                                            onClick={() => handleGetAiReview(internship._id)}
                                            disabled={aiLoadingId === internship._id}
                                            className="flex items-center gap-2 text-primary-600 font-bold text-xs bg-primary-50 px-4 py-2 rounded-xl hover:bg-primary-100 transition-colors disabled:opacity-50"
                                        >
                                            {aiLoadingId === internship._id ? (
                                                <Loader2 className="w-4 h-4 animate-spin" />
                                            ) : (
                                                <Sparkles className="w-4 h-4" />
                                            )}
                                            {internship.ai_review ? 'Refresh AI Review' : 'Get AI Review & Tips'}
                                        </button>
                                    </div>
                                </div>

                                <div className="flex md:flex-col justify-end gap-2 shrink-0">
                                    <button
                                        onClick={() => { setSelectedInternship(internship); setFormData(internship); setIsEditing(true); setShowModal(true); }}
                                        className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                                    >
                                        <Edit3 className="w-5 h-5" />
                                    </button>
                                    <button
                                        onClick={() => deleteInternship(internship._id)}
                                        className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all"
                                    >
                                        <Trash2 className="w-5 h-5" />
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="text-center py-20 bg-gray-50 rounded-3xl border-2 border-dashed border-gray-200">
                        <Briefcase className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <h3 className="text-xl font-bold text-gray-700 mb-2">Start your journey!</h3>
                        <p className="text-gray-500 max-w-md mx-auto mb-8">
                            Keep track of all your internship applications in one place. AI Consular will help you optimize your chances.
                        </p>
                        <Button onClick={() => setShowModal(true)}>Add your first application</Button>
                    </div>
                )}
            </div>

            {/* Modal */}
            {showModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
                    <div className="bg-white rounded-3xl w-full max-w-lg overflow-hidden shadow-2xl">
                        <div className="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                            <h2 className="text-xl font-extrabold text-gray-900">
                                {isEditing ? 'Update Application' : 'Add New Application'}
                            </h2>
                            <button onClick={() => setShowModal(false)} className="text-gray-400 hover:text-gray-600 p-1">
                                <X className="w-6 h-6" />
                            </button>
                        </div>
                        <form onSubmit={handleSubmit} className="p-6 space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="col-span-2">
                                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-1.5">Company Name</label>
                                    <input
                                        type="text" required
                                        className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 outline-none"
                                        placeholder="e.g. Google, Microsoft, Startup X"
                                        value={formData.company}
                                        onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-1.5">Role</label>
                                    <input
                                        type="text" required
                                        className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 outline-none"
                                        placeholder="e.g. SDE Intern"
                                        value={formData.role}
                                        onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-1.5">Domain</label>
                                    <input
                                        type="text" required
                                        className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 outline-none"
                                        placeholder="e.g. Backend, Frontend"
                                        value={formData.domain}
                                        onChange={(e) => setFormData({ ...formData, domain: e.target.value })}
                                    />
                                </div>
                                <div className="col-span-2">
                                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-1.5">Status</label>
                                    <select
                                        className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 outline-none"
                                        value={formData.status}
                                        onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                                    >
                                        <option value="applied">Applied</option>
                                        <option value="interviewing">Interviewing</option>
                                        <option value="offered">Offered</option>
                                        <option value="rejected">Rejected</option>
                                    </select>
                                </div>
                                <div className="col-span-2">
                                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-1.5">Notes (Optional)</label>
                                    <textarea
                                        className="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 outline-none h-24 resize-none"
                                        placeholder="Add details about interview rounds, feedback, etc."
                                        value={formData.notes}
                                        onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                                    />
                                </div>
                            </div>
                            <div className="flex gap-3 pt-4">
                                <Button type="button" variant="outline" className="flex-grow" onClick={() => setShowModal(false)}>Cancel</Button>
                                <Button type="submit" className="flex-grow">{isEditing ? 'Save Changes' : 'Add Application'}</Button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default InternshipTracker;

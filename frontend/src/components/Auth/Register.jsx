import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserPlus, Loader2, GraduationCap } from 'lucide-react';
import api from '../../utils/api';
import { setToken, setUser } from '../../utils/auth';
import { BRANCHES, YEARS, CAREER_GOALS } from '../../utils/constants';
import Card from '../UI/Card';

const Register = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        branch: '',
        year: 1,
        interests: '',
        career_goal: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            // Convert interests from comma-separated string to array
            const interests = formData.interests
                .split(',')
                .map(i => i.trim())
                .filter(i => i);

            const response = await api.post('/api/auth/register', {
                ...formData,
                interests,
                year: parseInt(formData.year)
            });

            const { access_token, user } = response.data;

            setToken(access_token);
            setUser(user);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const inputClasses = "w-full px-4 py-3 bg-surface-light/50 border border-white/10 rounded-xl text-white placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-secondary/50 focus:border-transparent transition-all";
    const labelClasses = "text-sm font-medium text-text-secondary ml-1";

    return (
        <div className="min-h-screen flex items-center justify-center p-4 py-12">
            <div className="w-full max-w-2xl relative z-10">
                {/* Header */}
                <div className="text-center mb-8 animate-fade-in">
                    <div className="inline-flex p-3 bg-gradient-to-br from-secondary to-secondary-dim rounded-2xl shadow-lg shadow-secondary/20 mb-4">
                        <GraduationCap className="w-10 h-10 text-white" />
                    </div>
                    <h1 className="text-4xl font-heading font-bold text-white mb-2 tracking-tight">
                        Start Your Journey
                    </h1>
                    <p className="text-text-secondary">
                        Create your personalized academic profile
                    </p>
                </div>

                {/* Register Card */}
                <Card className="animate-slide-up border-secondary/10">
                    {error && (
                        <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl">
                            <p className="text-sm text-red-400 text-center">{error}</p>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                            <div className="space-y-1.5">
                                <label className={labelClasses}>Full Name</label>
                                <input
                                    type="text"
                                    name="name"
                                    value={formData.name}
                                    onChange={handleChange}
                                    className={inputClasses}
                                    placeholder="John Doe"
                                    required
                                />
                            </div>

                            <div className="space-y-1.5">
                                <label className={labelClasses}>Email</label>
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    className={inputClasses}
                                    placeholder="name@example.com"
                                    required
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                            <div className="space-y-1.5">
                                <label className={labelClasses}>Branch</label>
                                <div className="relative">
                                    <select
                                        name="branch"
                                        value={formData.branch}
                                        onChange={handleChange}
                                        className={`${inputClasses} appearance-none cursor-pointer`}
                                        required
                                    >
                                        <option value="" className="bg-surface-light text-text-muted">Select Branch</option>
                                        {BRANCHES.map(branch => (
                                            <option key={branch} value={branch} className="bg-surface-light text-white">{branch}</option>
                                        ))}
                                    </select>
                                    <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-text-muted">
                                        ▼
                                    </div>
                                </div>
                            </div>

                            <div className="space-y-1.5">
                                <label className={labelClasses}>Year</label>
                                <div className="relative">
                                    <select
                                        name="year"
                                        value={formData.year}
                                        onChange={handleChange}
                                        className={`${inputClasses} appearance-none cursor-pointer`}
                                        required
                                    >
                                        {YEARS.map(year => (
                                            <option key={year} value={year} className="bg-surface-light text-white">{year} Year</option>
                                        ))}
                                    </select>
                                    <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-text-muted">
                                        ▼
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="space-y-1.5">
                            <label className={labelClasses}>Career Goal</label>
                            <div className="relative">
                                <select
                                    name="career_goal"
                                    value={formData.career_goal}
                                    onChange={handleChange}
                                    className={`${inputClasses} appearance-none cursor-pointer`}
                                    required
                                >
                                    <option value="" className="bg-surface-light text-text-muted">Select Goal</option>
                                    {CAREER_GOALS.map(goal => (
                                        <option key={goal} value={goal} className="bg-surface-light text-white">{goal}</option>
                                    ))}
                                </select>
                                <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-text-muted">
                                    ▼
                                </div>
                            </div>
                        </div>

                        <div className="space-y-1.5">
                            <label className={labelClasses}>
                                Interests <span className="text-text-muted font-normal">(comma-separated)</span>
                            </label>
                            <input
                                type="text"
                                name="interests"
                                value={formData.interests}
                                onChange={handleChange}
                                className={inputClasses}
                                placeholder="e.g. Machine Learning, IoT, Web Design"
                            />
                        </div>

                        <div className="space-y-1.5">
                            <label className={labelClasses}>Password</label>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                className={inputClasses}
                                placeholder="Create a strong password"
                                minLength="6"
                                required
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-3.5 mt-2 bg-gradient-to-r from-secondary to-secondary-dim hover:to-secondary text-white font-medium rounded-xl shadow-lg shadow-secondary/25 hover:shadow-secondary/40 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed group"
                        >
                            {loading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <>
                                    <span>Create Account</span>
                                    <UserPlus className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                </>
                            )}
                        </button>
                    </form>

                    <div className="mt-8 text-center">
                        <p className="text-sm text-text-muted">
                            Already have an account?{' '}
                            <Link to="/login" className="text-secondary-glow hover:text-white font-medium transition-colors">
                                Sign in here
                            </Link>
                        </p>
                    </div>
                </Card>
            </div>
        </div>
    );
};

export default Register;

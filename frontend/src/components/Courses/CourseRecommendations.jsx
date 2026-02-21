import { useState, useEffect } from 'react';
import { BookOpen, Clock, Award, ExternalLink, TrendingUp } from 'lucide-react';
import api from '../../utils/api';

const CourseRecommendations = () => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [filter, setFilter] = useState('recommended');

    useEffect(() => {
        fetchCourses();
    }, [filter]);

    const fetchCourses = async () => {
        setLoading(true);
        setError('');

        try {
            let endpoint = '/api/courses/all';
            if (filter === 'recommended') endpoint = '/api/courses/recommendations';
            if (filter === 'enrolled') endpoint = '/api/courses/enrolled';

            const response = await api.get(endpoint);
            setCourses(response.data);
        } catch (err) {
            console.error('Failed to fetch courses:', err);
            setError('Failed to load courses. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const getDifficultyColor = (difficulty) => {
        switch (difficulty?.toLowerCase()) {
            case 'beginner': return 'bg-green-100 text-green-800';
            case 'intermediate': return 'bg-yellow-100 text-yellow-800';
            case 'advanced': return 'bg-red-100 text-red-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    const enrollInCourse = async (courseId) => {
        try {
            const response = await api.post(`/api/courses/${courseId}/enroll`);
            if (response.data.success) {
                // Refresh courses to update UI if needed, or just show success
                alert("Successfully enrolled in course!");
                // Optionally refresh if we want to update the "enrolled" status visually immediately
                // For now, simpler is better.
            }
        } catch (err) {
            console.error('Enrollment failed:', err);
            alert("Failed to enroll. Please try again.");
        }
    };

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center py-20 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
                <p className="mt-4 text-gray-300">Loading courses...</p>
            </div>
        );
    }

    return (
        <div className="py-4">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-white mb-2">Course Recommendations</h1>
                    <p className="text-gray-400">Personalized courses based on your interests and career goals</p>
                </div>

                <div className="mb-6 flex gap-4">
                    <button
                        onClick={() => setFilter('recommended')}
                        className={`px-6 py-2 rounded-lg font-medium transition-colors ${filter === 'recommended' ? 'bg-primary-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'
                            }`}
                    >
                        <TrendingUp className="w-4 h-4 inline mr-2" />
                        Recommended for You
                    </button>
                    <button
                        onClick={() => setFilter('all')}
                        className={`px-6 py-2 rounded-lg font-medium transition-colors ${filter === 'all' ? 'bg-primary-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'
                            }`}
                    >
                        <BookOpen className="w-4 h-4 inline mr-2" />
                        All Courses
                    </button>
                    <button
                        onClick={() => setFilter('enrolled')}
                        className={`px-6 py-2 rounded-lg font-medium transition-colors ${filter === 'enrolled' ? 'bg-primary-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'
                            }`}
                    >
                        <Award className="w-4 h-4 inline mr-2" />
                        My Courses
                    </button>
                </div>

                {error && (
                    <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                        <p className="text-red-600">{error}</p>
                    </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {courses.map((course) => (
                        <div key={course._id} className="bg-surface/50 backdrop-blur-md border border-white/10 rounded-xl p-6 hover:shadow-lg hover:border-primary/30 transition-all group">
                            <div className="mb-4">
                                <div className="flex items-start justify-between mb-2">
                                    <h3 className="text-lg font-semibold text-white flex-1">{course.title}</h3>
                                    {course.relevance_score > 0 && filter === 'recommended' && (
                                        <span className="ml-2 px-2 py-1 bg-primary-500/20 text-primary-300 text-xs font-medium rounded border border-primary-500/30">
                                            {course.relevance_score}★
                                        </span>
                                    )}
                                </div>
                                <p className="text-sm text-gray-300">{course.platform}</p>
                            </div>

                            <div className="space-y-3 mb-4">
                                <div className="flex items-center text-sm text-gray-300">
                                    <BookOpen className="w-4 h-4 mr-2 text-primary-400" />
                                    <span>{course.domain}</span>
                                </div>
                                <div className="flex items-center text-sm text-gray-300">
                                    <Clock className="w-4 h-4 mr-2 text-primary-400" />
                                    <span>{course.duration}</span>
                                </div>
                                <div className="flex items-center">
                                    <Award className="w-4 h-4 mr-2 text-primary-400" />
                                    <span className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(course.difficulty)}`}>
                                        {course.difficulty}
                                    </span>
                                </div>
                            </div>

                            <div className="mb-4">
                                <p className="text-xs font-medium text-gray-400 mb-2">Skills:</p>
                                <div className="flex flex-wrap gap-2">
                                    {course.skills?.slice(0, 3).map((skill, index) => (
                                        <span key={index} className="px-2 py-1 bg-white/10 text-gray-200 text-xs rounded border border-white/5">
                                            {skill}
                                        </span>
                                    ))}
                                    {course.skills?.length > 3 && (
                                        <span className="px-2 py-1 bg-white/10 text-gray-200 text-xs rounded border border-white/5">
                                            +{course.skills.length - 3} more
                                        </span>
                                    )}
                                </div>
                            </div>

                            <div className="flex gap-2">
                                <a
                                    href={course.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="btn-secondary flex-1 flex items-center justify-center gap-2 text-sm"
                                >
                                    View
                                    <ExternalLink className="w-3 h-3" />
                                </a>
                                {filter !== 'enrolled' && (
                                    <button
                                        onClick={() => enrollInCourse(course._id)}
                                        className="btn-primary flex-1 text-sm bg-primary-600 hover:bg-primary-700 text-white"
                                    >
                                        Enroll
                                    </button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>

                {!loading && courses.length === 0 && (
                    <div className="text-center py-12">
                        <BookOpen className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                        <h3 className="text-lg font-medium text-white mb-2">No courses found</h3>
                        <p className="text-gray-400">Try changing your filter or check back later.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CourseRecommendations;

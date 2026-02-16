import { useState } from 'react';
import { Upload, FileText, Send, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import api from '../../utils/api';
import Card from '../shared/Card';
import Button from '../shared/Button';

const ResumeATS = () => {
    const [file, setFile] = useState(null);
    const [jobDescription, setJobDescription] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile && selectedFile.type === 'application/pdf') {
            setFile(selectedFile);
            setError('');
        } else {
            setFile(null);
            setError('Please select a valid PDF file.');
        }
    };

    const handleAnalyze = async (e) => {
        e.preventDefault();
        if (!file) {
            setError('Please upload your resume (PDF) for analysis.');
            return;
        }

        setError('');
        setLoading(true);
        setResult(null);

        try {
            const formData = new FormData();
            formData.append('file', file);
            if (jobDescription) {
                formData.append('job_description', jobDescription);
            }

            const response = await api.post('/api/resume/ats-check-upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setResult(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to analyze resume. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto py-8 px-4">
            <h1 className="text-3xl font-bold text-white mb-2">Resume ATS Optimizer</h1>
            <p className="text-gray-300 mb-8">
                Boost your chances of getting hired by analyzing your resume against industry standards and specific job descriptions.
            </p>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                <Card className="bg-surface/60 backdrop-blur-md border border-white/20 p-5">
                    <h3 className="text-lg font-bold text-white mb-4">Resume Upload</h3>
                    <div className="flex flex-col items-center justify-center h-64 border-2 border-dashed border-white/20 rounded-lg bg-gray-800/30 hover:bg-gray-800/50 transition-colors">
                        <input
                            type="file"
                            id="resume-upload"
                            className="hidden"
                            accept=".pdf"
                            onChange={handleFileChange}
                        />
                        <label
                            htmlFor="resume-upload"
                            className="flex flex-col items-center cursor-pointer p-6 text-center"
                        >
                            {file ? (
                                <>
                                    <FileText className="w-16 h-16 text-primary-400 mb-3" />
                                    <span className="text-white font-medium">{file.name}</span>
                                    <span className="text-gray-400 text-sm mt-1">Click to change file</span>
                                </>
                            ) : (
                                <>
                                    <Upload className="w-16 h-16 text-gray-400 mb-3" />
                                    <span className="text-white font-medium">Click to upload or drag and drop</span>
                                    <span className="text-gray-400 text-sm mt-1">Support for PDF only</span>
                                </>
                            )}
                        </label>
                    </div>
                </Card>

                <Card className="bg-surface/60 backdrop-blur-md border border-white/20 p-5">
                    <h3 className="text-lg font-bold text-white mb-4">Job Description (Optional)</h3>
                    <textarea
                        className="w-full h-64 p-3 bg-gray-800/50 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                        placeholder="Paste the job description here for better matching..."
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                    ></textarea>
                </Card>
            </div>

            <div className="flex justify-center mb-12">
                <Button
                    onClick={handleAnalyze}
                    className="px-8 py-3 text-lg shadow-lg shadow-primary-600/20"
                    disabled={loading || !file}
                >
                    {loading ? (
                        <div className="flex items-center gap-2">
                            <Loader2 className="w-5 h-5 animate-spin" />
                            Analyzing...
                        </div>
                    ) : (
                        <div className="flex items-center gap-2">
                            <Send className="w-5 h-5" />
                            Run ATS Check
                        </div>
                    )}
                </Button>
            </div>

            {error && (
                <div className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 mb-8 flex items-center gap-3">
                    <AlertCircle className="w-5 h-5 shrink-0" />
                    {error}
                </div>
            )}

            {result && (
                <div className="space-y-8 animate-fade-in">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <Card className="bg-surface/60 border border-white/10 p-6 text-center">
                            <p className="text-sm text-gray-400 mb-1">ATS Score</p>
                            <div className={`text-4xl font-black ${result.ats_score > 80 ? 'text-green-400' : result.ats_score > 60 ? 'text-orange-400' : 'text-red-400'}`}>
                                {result.ats_score}%
                            </div>
                        </Card>
                        <Card className="bg-surface/60 border border-white/10 p-6 text-center">
                            <p className="text-sm text-gray-400 mb-1">Keywords Found</p>
                            <div className="text-3xl font-bold text-blue-400">
                                {result.keywords_found?.length || 0}
                            </div>
                        </Card>
                        <Card className="bg-surface/60 border border-white/10 p-6 text-center">
                            <p className="text-sm text-gray-400 mb-1">Missing Keywords</p>
                            <div className="text-3xl font-bold text-red-400">
                                {result.keywords_missing?.length || 0}
                            </div>
                        </Card>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <Card className="bg-surface/60 border border-white/10 p-6">
                            <div className="flex items-center gap-3 mb-4">
                                <CheckCircle className="text-green-400 w-5 h-5" />
                                <h3 className="font-bold text-white">Keywords Found</h3>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {result.keywords_found?.map((kw, i) => (
                                    <span key={i} className="px-3 py-1 bg-green-500/20 text-green-300 rounded-full text-xs font-medium border border-green-500/30">
                                        {kw}
                                    </span>
                                ))}
                                {(!result.keywords_found || result.keywords_found.length === 0) && (
                                    <p className="text-gray-500 text-sm italic">No specific keywords identified.</p>
                                )}
                            </div>
                        </Card>

                        <Card className="bg-surface/60 border border-white/10 p-6">
                            <div className="flex items-center gap-3 mb-4">
                                <AlertCircle className="text-red-400 w-5 h-5" />
                                <h3 className="font-bold text-white">Keywords to Add</h3>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {result.keywords_missing?.map((kw, i) => (
                                    <span key={i} className="px-3 py-1 bg-red-500/20 text-red-300 rounded-full text-xs font-medium border border-red-500/30">
                                        {kw}
                                    </span>
                                ))}
                                {(!result.keywords_missing || result.keywords_missing.length === 0) && (
                                    <p className="text-gray-500 text-sm italic">Great! No major keywords are missing.</p>
                                )}
                            </div>
                        </Card>
                    </div>

                    <Card className="bg-surface/60 border border-white/10 p-6">
                        <h3 className="font-bold text-white mb-4">Improvement Suggestions</h3>
                        <ul className="space-y-4">
                            {result.suggestions?.map((sug, i) => (
                                <li key={i} className="flex items-start gap-3 text-gray-200">
                                    <div className="mt-2 w-1.5 h-1.5 rounded-full bg-primary-500 shrink-0 shadow-[0_0_8px_rgba(6,182,212,0.6)]"></div>
                                    {sug}
                                </li>
                            ))}
                        </ul>
                    </Card>
                </div>
            )}
        </div>
    );
};

export default ResumeATS;

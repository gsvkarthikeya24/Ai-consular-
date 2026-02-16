import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated } from './utils/auth';

// Components
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import StudentDashboard from './components/Dashboard/StudentDashboard';
import AdminDashboard from './components/Admin/AdminDashboard';
import ResumeATS from './components/Resume/ResumeATS';
import CareerCounselor from './components/Career/CareerCounselor';
import AIMentor from './components/Mentor/AIMentor';
import TaskList from './components/Tasks/TaskList';
import TaskDetail from './components/Tasks/TaskDetail';
import InterviewPrep from './components/Interview/InterviewPrep';
import InternshipTracker from './components/Internships/InternshipTracker';
import ProgressAnalytics from './components/Dashboard/ProgressAnalytics';
import CourseRecommendations from './components/Courses/CourseRecommendations';
import GATEPrep from './components/GATE/GATEPrep';
import BranchQuiz from './components/Career/BranchQuiz';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import BackgroundEffect from './components/UI/BackgroundEffect';
import Footer from './components/shared/Footer';

function App() {
    return (
        <BrowserRouter>
            <BackgroundEffect />
            <Footer />
            <Routes>
                {/* Public Routes - No longer redirecting away */}
                <Route
                    path="/login"
                    element={<Login />}
                />
                <Route
                    path="/register"
                    element={<Register />}
                />


                {/* Protected Routes */}
                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <StudentDashboard />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/career"
                    element={
                        <ProtectedRoute>
                            <CareerCounselor />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/branch-quiz"
                    element={
                        <ProtectedRoute>
                            <BranchQuiz />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/resume"
                    element={
                        <ProtectedRoute>
                            <ResumeATS />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/mentor"
                    element={
                        <ProtectedRoute>
                            <AIMentor />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/tasks"
                    element={
                        <ProtectedRoute>
                            <TaskList />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/tasks/:id"
                    element={
                        <ProtectedRoute>
                            <TaskDetail />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/interview"
                    element={
                        <ProtectedRoute>
                            <InterviewPrep />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/internships"
                    element={
                        <ProtectedRoute>
                            <InternshipTracker />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/courses"
                    element={
                        <ProtectedRoute>
                            <CourseRecommendations />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/gate"
                    element={
                        <ProtectedRoute>
                            <GATEPrep />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/analytics"
                    element={
                        <ProtectedRoute>
                            <ProgressAnalytics />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/admin"
                    element={
                        <ProtectedRoute requireAdmin>
                            <AdminDashboard />
                        </ProtectedRoute>
                    }
                />

                {/* Default Route */}
                <Route
                    path="/"
                    element={<Navigate to={isAuthenticated() ? "/dashboard" : "/login"} />}
                />

                {/* 404 Route */}
                <Route path="*" element={<Navigate to="/" />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;

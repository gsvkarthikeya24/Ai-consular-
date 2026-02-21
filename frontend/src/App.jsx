import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

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
import Layout from './components/shared/Layout';

/** Inner app — has access to AuthContext */
function AppRoutes() {
    const { isLoggedIn, authState } = useAuth();

    if (authState === 'loading') {
        return null; // Layout handled by ProtectedRoute/Spinner
    }

    return (
        <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected Routes — Wrapped in Layout */}
            <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
                <Route path="/dashboard" element={<StudentDashboard />} />
                <Route path="/career" element={<CareerCounselor />} />
                <Route path="/branch-quiz" element={<BranchQuiz />} />
                <Route path="/resume" element={<ResumeATS />} />
                <Route path="/mentor" element={<AIMentor />} />
                <Route path="/tasks" element={<TaskList />} />
                <Route path="/tasks/:id" element={<TaskDetail />} />
                <Route path="/interview" element={<InterviewPrep />} />
                <Route path="/internships" element={<InternshipTracker />} />
                <Route path="/courses" element={<CourseRecommendations />} />
                <Route path="/gate" element={<GATEPrep />} />
                <Route path="/analytics" element={<ProgressAnalytics />} />
                <Route
                    path="/admin"
                    element={
                        <ProtectedRoute requireAdmin>
                            <AdminDashboard />
                        </ProtectedRoute>
                    }
                />
            </Route>

            {/* Default Route */}
            <Route path="/" element={<Navigate to={isLoggedIn ? "/dashboard" : "/login"} replace />} />

            {/* 404 Route */}
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
}

function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <AppRoutes />
            </AuthProvider>
        </BrowserRouter>
    );
}

export default App;

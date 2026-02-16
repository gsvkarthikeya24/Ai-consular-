// Authentication utilities

export const setToken = (token) => {
    localStorage.setItem('access_token', token);
};

export const getToken = () => {
    return localStorage.getItem('access_token');
};

export const removeToken = () => {
    localStorage.removeItem('access_token');
};

export const setUser = (user) => {
    localStorage.setItem('user', JSON.stringify(user));
};

export const getUser = () => {
    const user = localStorage.getItem('user');
    if (user) return JSON.parse(user);

    // Default mock user for "Demo Mode" without login
    return {
        _id: "demo_student_123",
        name: "Demo Student",
        email: "student1@example.com",
        branch: "Computer Science",
        year: 3,
        career_goal: "Software Engineer",
        interests: ["AI", "Web Development", "Cloud"]
    };
};

export const removeUser = () => {
    localStorage.removeItem('user');
};

export const logout = () => {
    removeToken();
    removeUser();
    // Redirect to root instead of login
    window.location.href = '/';
};

export const isAuthenticated = () => {
    return true; // Always authenticated for easy access
};

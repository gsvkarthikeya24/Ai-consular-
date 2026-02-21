// Authentication utilities

const parseJwt = (token) => {
    try {
        if (!token) return null;
        const base64Url = token.split('.')[1];
        if (!base64Url) return null;

        // Fix base64 padding
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const pad = base64.length % 4;
        const paddedBase64 = pad ? base64 + '='.repeat(4 - pad) : base64;

        const jsonPayload = decodeURIComponent(atob(paddedBase64).split('').map(function (c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        return JSON.parse(jsonPayload);
    } catch (e) {
        console.error("JWT parsing error:", e);
        return null;
    }
};

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
    try {
        const user = localStorage.getItem('user');
        if (user) return JSON.parse(user);
    } catch (e) {
        console.error("Failed to parse user from localStorage", e);
    }

    return null;
};

export const removeUser = () => {
    localStorage.removeItem('user');
};

export const logout = () => {
    removeToken();
    removeUser();
    // Redirect to login page explicitly on logout
    window.location.href = '/login';
};

export const isAuthenticated = () => {
    const token = getToken();
    const user = getUser();

    if (!token || !user) return false;

    // Check if token is expired
    const payload = parseJwt(token);

    // If we can't parse the payload, consider it unauthenticated
    if (!payload || !payload.exp) {
        return false;
    }

    const currentTime = Math.floor(Date.now() / 1000);
    // Token is valid if expiration is in the future
    if (payload.exp < currentTime) {
        return false;
    }

    return true;
};

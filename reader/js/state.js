// state.js - Centralized state management
export const State = {
    currentPage: 1,
    totalPages: 1313,
    currentView: localStorage.getItem('readerView') || 'image',
    menuOpen: false,
    pageData: {},
    manifest: null,

    listeners: new Map(),

    subscribe(key, callback) {
        if (!this.listeners.has(key)) {
            this.listeners.set(key, []);
        }
        this.listeners.get(key).push(callback);
    },

    set(key, value) {
        this[key] = value;
        if (this.listeners.has(key)) {
            this.listeners.get(key).forEach(cb => cb(value));
        }
    },

    get(key) {
        return this[key];
    }
};

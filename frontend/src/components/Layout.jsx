import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  LayoutDashboard, 
  UploadCloud, 
  History, 
  User, 
  LogOut, 
  Sun, 
  Moon, 
  Menu, 
  X, 
  Sprout 
} from 'lucide-react';

export const Layout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(
    localStorage.getItem('theme') === 'dark' || 
    (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)
  );

  // Apply dark mode class to document node
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { label: 'Upload Scan', path: '/upload', icon: UploadCloud },
    { label: 'Scan History', path: '/history', icon: History },
    { label: 'My Profile', path: '/profile', icon: User },
  ];

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 flex flex-col transition-colors duration-300">
      {/* Top Navbar */}
      <header className="sticky top-0 z-40 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200/80 dark:border-slate-800/80 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button 
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-1.5 rounded-lg md:hidden hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          
          <Link to="/" className="flex items-center gap-2 font-bold text-xl text-brand-600 dark:text-brand-500 tracking-tight">
            <div className="bg-brand-100 dark:bg-brand-500/10 p-1.5 rounded-xl">
              <Sprout className="text-brand-600 dark:text-brand-500" size={24} />
            </div>
            <span>LeafSense <span className="text-slate-400 font-light">AI</span></span>
          </Link>
        </div>

        <div className="flex items-center gap-4">
          {/* Theme Toggle Button */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all text-slate-600 dark:text-slate-300"
            title="Toggle theme"
          >
            {darkMode ? <Sun size={18} /> : <Moon size={18} />}
          </button>

          {user && (
            <div className="hidden sm:flex items-center gap-2 text-sm border-l border-slate-200 dark:border-slate-800 pl-4">
              <div className="bg-gradient-to-tr from-brand-600 to-emerald-500 text-white w-8 h-8 rounded-xl flex items-center justify-center font-bold shadow-md shadow-brand-500/10">
                {user.username.charAt(0).toUpperCase()}
              </div>
              <span className="font-medium text-slate-600 dark:text-slate-300">{user.username}</span>
            </div>
          )}
        </div>
      </header>

      <div className="flex-1 flex relative">
        {/* Sidebar Navigation */}
        <aside className={`
          fixed inset-y-0 left-0 top-[57px] z-30 w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800/80 p-4 flex flex-col justify-between transform transition-transform duration-300 ease-in-out md:translate-x-0 md:sticky md:h-[calc(100vh-57px)]
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        `}>
          <div className="space-y-6">
            <div className="space-y-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setSidebarOpen(false)}
                    className={`
                      flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all group
                      ${isActive(item.path) 
                        ? 'bg-brand-500 text-white shadow-lg shadow-brand-500/15' 
                        : 'hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100'}
                    `}
                  >
                    <Icon 
                      size={18} 
                      className={`transition-transform duration-200 group-hover:scale-110 ${isActive(item.path) ? 'text-white' : 'text-slate-400 dark:text-slate-500 group-hover:text-brand-500'}`} 
                    />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          {/* Logout section at bottom of sidebar */}
          <div className="border-t border-slate-100 dark:border-slate-800/50 pt-4">
            <button
              onClick={handleLogout}
              className="flex items-center gap-3 w-full px-4 py-3 rounded-xl text-sm font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-500/10 hover:text-red-700 transition-all group"
            >
              <LogOut size={18} className="text-red-400 dark:text-red-500 group-hover:translate-x-0.5 transition-transform" />
              <span>Log Out</span>
            </button>
          </div>
        </aside>

        {/* Overlay for mobile drawer */}
        {sidebarOpen && (
          <div 
            onClick={() => setSidebarOpen(false)}
            className="fixed inset-0 top-[57px] z-20 bg-slate-950/20 backdrop-blur-sm md:hidden"
          />
        )}

        {/* Page Content Viewport */}
        <main className="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full overflow-x-hidden">
          {children}
        </main>
      </div>
    </div>
  );
};

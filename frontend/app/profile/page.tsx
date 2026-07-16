'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function ProfilePage() {
    const router = useRouter()
    const [mainMenuOpen, setMainMenuOpen] = useState(false)

    useEffect(() => {
        const token = typeof window !== 'undefined' ? localStorage.getItem('mb_token') : null
        if (!token) {
            router.replace('/login')
        }
    }, [router])

    const handleLogout = (e: React.MouseEvent) => {
        e.preventDefault()
        localStorage.clear()
        router.replace('/login')
    }

    return (
        <div className="bg-immersive min-h-screen flex flex-col font-body-md text-on-background relative" style={{ zoom: 0.90 }}>
            {/* Background Grain and Ambient Blobs */}
            <div className="bg-grain"></div>
            <div className="fixed top-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-slate-300/40 mix-blend-multiply filter blur-[120px] pointer-events-none z-0"></div>
            <div className="fixed bottom-[-10%] right-[-10%] w-[60vw] h-[60vw] rounded-full bg-stone-200/50 mix-blend-multiply filter blur-[120px] pointer-events-none z-0"></div>
            
            {/* TopAppBar */}
            <header className="fixed top-0 z-40 flex justify-between items-center w-full px-4 md:px-margin-desktop py-4 pointer-events-none animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
                <div className="flex items-center gap-4 pointer-events-auto">
                    <span className="text-headline-md font-headline-md font-medium text-primary ml-2 md:ml-0">Mythri</span>
                </div>
                <div className="flex items-center gap-4 relative pointer-events-auto mr-2 md:mr-0">
                    <button 
                        onClick={() => setMainMenuOpen(!mainMenuOpen)}
                        className="hidden md:block material-symbols-outlined text-primary hover:bg-surface-container-high p-2 rounded-full transition-all active:scale-95"
                    >
                        grid_view
                    </button>
                    
                    {/* Desktop Dropdown Menu */}
                    <nav className={`absolute right-0 top-[100%] mt-2 w-56 bg-white/70 backdrop-blur-3xl border border-white/50 shadow-2xl rounded-2xl flex-col p-2 gap-1 origin-top transition-all duration-300 hidden md:flex ${mainMenuOpen ? 'scale-y-100 opacity-100 pointer-events-auto' : 'scale-y-0 opacity-0 pointer-events-none'}`}>
                        <Link href="/" className="text-on-surface-variant hover:bg-white/60 transition-colors px-4 py-2.5 rounded-xl flex items-center gap-3 font-label-md">
                            <span className="material-symbols-outlined text-[20px]">home</span> Sanctuary
                        </Link>
                        <Link href="/consultation" className="text-on-surface-variant hover:bg-white/60 transition-colors px-4 py-2.5 rounded-xl flex items-center gap-3 font-label-md">
                            <span className="material-symbols-outlined text-[20px]">health_and_safety</span> Consultation
                        </Link>
                        <Link href="/history" className="text-on-surface-variant hover:bg-white/60 transition-colors px-4 py-2.5 rounded-xl flex items-center gap-3 font-label-md">
                            <span className="material-symbols-outlined text-[20px]">history</span> Journal
                        </Link>
                        <Link href="/profile" className="text-primary font-bold bg-white/80 px-4 py-2.5 rounded-xl flex items-center gap-3 font-label-md">
                            <span className="material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>person</span> Profile
                        </Link>
                        <div className="h-px bg-outline-variant/30 my-1 mx-2"></div>
                        <button onClick={handleLogout} className="text-error hover:bg-error/10 transition-colors px-4 py-2.5 rounded-xl flex items-center gap-3 font-label-md text-left w-full">
                            <span className="material-symbols-outlined text-[20px]">logout</span> Logout
                        </button>
                    </nav>
                </div>
            </header>

            <main className="relative z-10 h-screen w-full max-w-screen-xl mx-auto px-4 md:px-margin-desktop pb-24 md:pb-8 flex flex-col md:flex-row gap-6 md:gap-8 lg:gap-16 pt-24 overflow-y-auto md:overflow-hidden animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
                
                {/* Left Sidebar: Profile Overview & Navigation */}
                <aside className="w-full md:w-1/4 flex flex-col gap-6 md:h-full md:overflow-y-auto hide-scrollbar shrink-0">
                    {/* User Card */}
                    <div className="w-full bg-white/50 backdrop-blur-3xl border border-outline-variant/30 shadow-sm rounded-3xl p-6 flex flex-col items-center relative overflow-hidden">
                        <div className="relative w-24 h-24 rounded-full bg-surface-container-high border-2 border-white shadow-md flex items-center justify-center mb-4">
                            <span className="material-symbols-outlined text-[48px] text-primary">person</span>
                            <button className="absolute bottom-0 right-0 bg-primary text-white p-1.5 rounded-full shadow hover:scale-105 transition-transform" title="Update Photo">
                                <span className="material-symbols-outlined text-[14px]">edit</span>
                            </button>
                        </div>
                        <h2 className="text-headline-md font-headline-md text-primary text-center">John Doe</h2>
                        <p className="text-body-sm font-body-sm text-on-surface-variant italic text-center">Explorer of the Mind</p>
                    </div>
                    {/* Vertical Navigation */}
                    <nav className="flex flex-col gap-2 w-full pb-8 md:pb-0">
                        <button className="w-full flex items-center gap-3 px-4 py-3 bg-white/70 backdrop-blur-md rounded-2xl border border-primary shadow-sm text-primary font-label-md transition-all">
                            <span className="material-symbols-outlined">person</span> Personal Info
                        </button>
                        <button className="w-full flex items-center gap-3 px-4 py-3 hover:bg-white/40 md:bg-white/40 border border-transparent rounded-2xl text-on-surface-variant font-label-md transition-all md:shadow-sm">
                            <span className="material-symbols-outlined">tune</span> Preferences
                        </button>
                        <button className="w-full flex items-center gap-3 px-4 py-3 hover:bg-white/40 md:bg-white/40 border border-transparent rounded-2xl text-on-surface-variant font-label-md transition-all md:shadow-sm">
                            <span className="material-symbols-outlined">security</span> Data & Privacy
                        </button>
                        <button className="w-full flex items-center gap-3 px-4 py-3 hover:bg-white/40 md:bg-white/40 border border-transparent rounded-2xl text-on-surface-variant font-label-md transition-all md:shadow-sm">
                            <span className="material-symbols-outlined">notifications</span> Notifications
                        </button>
                        <div className="md:hidden h-px bg-outline-variant/30 w-full my-1"></div>
                        <button onClick={handleLogout} className="md:hidden w-full flex items-center gap-3 px-4 py-3 bg-error-container/40 hover:bg-error-container/60 border border-transparent rounded-2xl text-error font-label-md transition-all shadow-sm active:scale-[0.98]">
                            <span className="material-symbols-outlined">logout</span> Log Out
                        </button>
                    </nav>
                </aside>

                {/* Right Content Area */}
                <section className="w-full md:w-3/4 md:h-full bg-white/50 backdrop-blur-2xl border border-white/50 shadow-xl rounded-3xl flex-col relative md:overflow-y-auto hide-scrollbar p-6 md:p-10 space-y-8 mb-8 md:mb-0 shrink-0">
                    <div>
                        <h1 className="text-headline-lg font-headline-lg text-primary mb-2">Personal Information</h1>
                        <p className="text-body-md text-on-surface-variant">Manage your basic profile details and how you present yourself in the Sanctuary.</p>
                    </div>
                    <div className="w-full h-px bg-outline-variant/30 my-2"></div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-white/60 border border-outline-variant/30 rounded-2xl p-5 flex flex-col gap-1 transition-all focus-within:ring-2 focus-within:ring-primary shadow-sm">
                            <span className="text-label-md font-label-md text-on-surface-variant uppercase tracking-widest opacity-70">Full Name</span>
                            <input type="text" className="text-headline-md font-headline-md text-on-surface bg-transparent outline-none w-full" defaultValue="John Doe" />
                        </div>
                        <div className="bg-white/60 border border-outline-variant/30 rounded-2xl p-5 flex flex-col gap-1 transition-all focus-within:ring-2 focus-within:ring-primary shadow-sm">
                            <span className="text-label-md font-label-md text-on-surface-variant uppercase tracking-widest opacity-70">Email Address</span>
                            <input type="email" className="text-headline-md font-headline-md text-on-surface bg-transparent outline-none w-full" defaultValue="john.doe@sanctuary.com" />
                        </div>
                        <div className="bg-white/60 border border-outline-variant/30 rounded-2xl p-5 flex flex-col gap-1 transition-all focus-within:ring-2 focus-within:ring-primary shadow-sm">
                            <span className="text-label-md font-label-md text-on-surface-variant uppercase tracking-widest opacity-70">Age</span>
                            <input type="number" className="text-headline-md font-headline-md text-on-surface bg-transparent outline-none w-full appearance-none" defaultValue="28" />
                        </div>
                        <div className="bg-white/60 border border-outline-variant/30 rounded-2xl p-5 flex flex-col gap-1 transition-all focus-within:ring-2 focus-within:ring-primary shadow-sm">
                            <span className="text-label-md font-label-md text-on-surface-variant uppercase tracking-widest opacity-70">Profession</span>
                            <input type="text" className="text-headline-md font-headline-md text-on-surface bg-transparent outline-none w-full" defaultValue="Designer" />
                        </div>
                    </div>

                    <div className="pt-6">
                        <h3 className="text-headline-md font-headline-md text-primary mb-4">Regional & Language</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="bg-white/60 border border-outline-variant/30 rounded-2xl p-5 flex flex-col gap-1 relative shadow-sm">
                                <span className="text-label-md font-label-md text-on-surface-variant uppercase tracking-widest opacity-70">Primary Language</span>
                                <select className="text-headline-md font-headline-md text-on-surface bg-transparent outline-none w-full appearance-none pr-8">
                                    <option>English</option>
                                    <option>Hindi</option>
                                    <option>Telugu</option>
                                    <option>Tamil</option>
                                </select>
                                <span className="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-on-surface-variant">expand_more</span>
                            </div>
                            <div className="bg-white/60 border border-outline-variant/30 rounded-2xl p-5 flex flex-col gap-1 relative shadow-sm">
                                <span className="text-label-md font-label-md text-on-surface-variant uppercase tracking-widest opacity-70">Timezone</span>
                                <select className="text-headline-md font-headline-md text-on-surface bg-transparent outline-none w-full appearance-none pr-8">
                                    <option>IST (UTC+05:30)</option>
                                    <option>GMT (UTC+00:00)</option>
                                    <option>EST (UTC-05:00)</option>
                                </select>
                                <span className="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-on-surface-variant">expand_more</span>
                            </div>
                        </div>
                    </div>

                    <div className="w-full flex justify-end gap-4 pt-6 border-t border-outline-variant/20 mt-8 mb-4">
                        <button className="px-6 py-3 rounded-2xl font-label-md text-label-md text-on-surface-variant border border-outline-variant hover:bg-white/70 transition-colors shadow-sm">Discard</button>
                        <button className="px-6 py-3 rounded-2xl font-label-md text-label-md text-white bg-primary hover:opacity-90 shadow-lg shadow-primary/20 transition-all active:scale-[0.98]">Save Changes</button>
                    </div>
                </section>
            </main>

            {/* BottomNavBar (Mobile Only) */}
            <nav className="md:hidden fixed bottom-0 w-full z-50 flex justify-around items-center bg-white/70 backdrop-blur-xl py-2 px-4 pb-safe shadow-[0_-4px_24px_rgba(0,0,0,0.05)] border-t border-white/40">
                <Link href="/" className="flex flex-col items-center justify-center text-on-surface-variant/60 w-16 transition-all duration-300 active:scale-90 active:opacity-70 px-5 py-1">
                    <span className="material-symbols-outlined text-[24px]">home</span>
                    <span className="text-[10px] font-label-md mt-1">Sanctuary</span>
                </Link>
                <Link href="/history" className="flex flex-col items-center justify-center text-on-surface-variant/60 w-16 transition-all duration-300 active:scale-90 active:opacity-70 px-5 py-1">
                    <span className="material-symbols-outlined text-[24px]">auto_stories</span>
                    <span className="text-[10px] font-label-md mt-1">Journal</span>
                </Link>
                <Link href="/consultation" className="flex flex-col items-center justify-center text-on-surface-variant/60 w-16 transition-all duration-300 active:scale-90 active:opacity-70 px-5 py-1">
                    <span className="material-symbols-outlined text-[24px]">health_and_safety</span>
                    <span className="text-[10px] font-label-md mt-1">Chat</span>
                </Link>
                <Link href="/profile" className="flex flex-col items-center justify-center text-primary w-16 transition-all duration-300 active:scale-90 px-5 py-1">
                    <div className="bg-primary text-white p-2.5 rounded-full shadow-lg transform -translate-y-3 flex items-center justify-center transition-transform duration-300 hover:scale-105 active:scale-95">
                        <span className="material-symbols-outlined text-[24px]" style={{ fontVariationSettings: "'FILL' 1" }}>person</span>
                    </div>
                    <span className="text-[10px] font-label-md font-bold -mt-2">Profile</span>
                </Link>
            </nav>
        </div>
    )
}

'use client'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function DashboardPage() {
  const router = useRouter()
  const [username, setUsername] = useState('Seeker')
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('mb_token')
    if (!token) {
      router.replace('/login')
    } else {
      const storedName = localStorage.getItem('mb_username')
      if (storedName) setUsername(storedName)
    }
  }, [router])

  return (
    <>
      {/* Desktop Top Nav */}
      <header className="hidden md:flex fixed top-0 z-40 justify-between items-center w-full px-margin-desktop py-4 pointer-events-none animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
        <div className="flex items-center gap-4 pointer-events-auto">
          <span className="text-headline-md font-headline-md font-medium text-primary">Mythri</span>
        </div>
        <div className="flex items-center gap-4 relative pointer-events-auto">
          <button onClick={() => setMenuOpen(!menuOpen)} className="material-symbols-outlined text-primary hover:bg-surface-container-high p-2 rounded-full transition-all active:scale-95">
            grid_view
          </button>
          
          {/* Dropdown Menu */}
          <nav className={`absolute right-0 top-[100%] mt-2 w-56 bg-white/70 backdrop-blur-3xl border border-white/50 shadow-2xl rounded-2xl flex flex-col p-2 gap-1 origin-top transition-all duration-300 ${menuOpen ? 'scale-y-100 opacity-100 pointer-events-auto' : 'scale-y-0 opacity-0 pointer-events-none'}`}>
            <Link href="/" className="text-primary font-bold bg-white/80 px-4 py-2.5 rounded-xl flex items-center gap-3 font-label-md">
              <span className="material-symbols-outlined text-[20px]">home</span> Sanctuary
            </Link>
            <Link href="/consultation" className="text-on-surface-variant hover:bg-white/60 transition-colors px-4 py-2.5 rounded-xl flex items-center gap-3 font-label-md">
              <span className="material-symbols-outlined text-[20px]">health_and_safety</span> Consultation
            </Link>
            <Link href="/history" className="text-on-surface-variant hover:bg-white/60 transition-colors px-4 py-2.5 rounded-xl flex items-center gap-3 font-label-md">
              <span className="material-symbols-outlined text-[20px]">history</span> Journal
            </Link>
            <Link href="/profile" className="text-on-surface-variant hover:bg-white/60 transition-colors px-4 py-2.5 rounded-xl flex items-center gap-3 font-label-md">
              <span className="material-symbols-outlined text-[20px]">person</span> Profile
            </Link>
            <div className="h-px bg-outline-variant/30 my-1 mx-2"></div>
            <button onClick={() => { localStorage.clear(); router.replace('/login'); }} className="text-error hover:bg-error/10 transition-colors px-4 py-2.5 rounded-xl flex items-center gap-3 font-label-md text-left w-full">
              <span className="material-symbols-outlined text-[20px]">logout</span> Logout
            </button>
          </nav>
        </div>
      </header>


      {/* Mobile Top Nav */}
      <header className="flex md:hidden fixed top-0 z-40 justify-between items-center w-full px-5 py-4 animate-fade-in-up bg-white/40 backdrop-blur-xl border-b border-white/50" style={{ animationDelay: '0.1s' }}>
        <div className="flex flex-col">
          <span className="text-body-sm text-on-surface-variant italic">Good morning,</span>
          <span className="text-headline-md font-headline-md font-medium text-primary">{username}</span>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={() => alert('No new notifications at this time.')} className="bg-white/60 p-2.5 rounded-full border border-white/80 shadow-sm text-primary hover:scale-105 active:scale-95 transition-transform">
            <span className="material-symbols-outlined text-[20px]">notifications</span>
          </button>
        </div>
      </header>

      {/* Desktop Main Content */}
      <main className="hidden md:flex h-[100dvh] w-full max-w-screen-xl mx-auto px-margin-desktop pb-6 pt-20 flex-col overflow-hidden animate-fade-in-up z-10" style={{ animationDelay: '0.2s' }}>
        <div className="mb-4 lg:mb-6 pl-2 shrink-0">
          <p className="text-body-lg text-on-surface-variant italic mb-1">Good morning,</p>
          <h1 className="text-display-lg font-headline-lg text-primary">{username}</h1>
        </div>

        <div className="flex flex-col md:flex-row gap-6 items-stretch w-full flex-1 min-h-0">
          {/* Left Column */}
          <section className="w-full md:w-5/12 flex flex-col min-h-0">
            <div className="flex-1 bg-white/60 backdrop-blur-2xl border border-white border-b-primary/10 shadow-lg shadow-primary/5 rounded-[2rem] p-8 lg:p-10 flex flex-col relative overflow-hidden transition-all duration-300 hover:shadow-xl min-h-0">
              <div className="absolute -right-12 -top-12 w-48 h-48 bg-primary/10 rounded-full blur-3xl pointer-events-none"></div>
              <h2 className="text-headline-lg font-headline-md text-primary mb-2 shrink-0">How are you feeling today?</h2>
              <p className="text-body-lg text-on-surface-variant mb-6 lg:mb-12 shrink-0">Take a moment to pause and center yourself before beginning your day.</p>
              
              <div className="grid grid-cols-2 gap-4 mt-auto flex-1 min-h-0">
                {['Calm', 'Focus', 'Anxious', 'Joyful'].map((mood, idx) => (
                  <button key={mood} onClick={() => router.push('/consultation')} className="h-full min-h-[100px] flex flex-col justify-center items-center gap-2 lg:gap-4 rounded-[1.5rem] bg-white/50 border border-outline-variant/30 hover:bg-white/80 active:scale-95 transition-all shadow-sm">
                    <span className="text-3xl lg:text-4xl drop-shadow-sm">{['😌', '🎯', '💭', '✨'][idx]}</span>
                    <span className="text-xs lg:text-sm font-label-md text-primary uppercase tracking-wider">{mood}</span>
                  </button>
                ))}
              </div>
            </div>
          </section>

          {/* Right Column */}
          <section className="w-full md:w-7/12 flex flex-col gap-4 lg:gap-6 min-h-0">
            <div className="grid grid-cols-2 gap-4 lg:gap-6 shrink-0">
              <Link href="/voice" className="bg-plum-high-contrast text-white p-5 lg:p-6 rounded-[1.5rem] flex items-center justify-between shadow-xl shadow-plum-high-contrast/20 hover:opacity-95 active:scale-[0.98] transition-all group">
                <div className="flex items-center gap-4 lg:gap-5">
                  <div className="w-12 h-12 lg:w-14 lg:h-14 rounded-full bg-white/20 flex items-center justify-center backdrop-blur-md transition-transform group-hover:scale-110">
                    <span className="material-symbols-outlined text-[24px] lg:text-[28px]">mic</span>
                  </div>
                  <div>
                    <h4 className="font-headline-md text-lg lg:text-xl">Voice Session</h4>
                    <p className="text-[12px] lg:text-[13px] opacity-80 font-body-sm mt-1">Speak freely</p>
                  </div>
                </div>
              </Link>
              <Link href="/history" className="bg-white/60 backdrop-blur-xl border border-white p-5 lg:p-6 rounded-[1.5rem] flex items-center justify-between shadow-sm hover:bg-white/90 active:scale-[0.98] transition-all group">
                <div className="flex items-center gap-4 lg:gap-5">
                  <div className="w-12 h-12 lg:w-14 lg:h-14 rounded-full bg-primary/10 flex items-center justify-center transition-transform group-hover:scale-110">
                    <span className="material-symbols-outlined text-[24px] lg:text-[28px] text-primary">edit_document</span>
                  </div>
                  <div>
                    <h4 className="font-headline-md text-lg lg:text-xl text-primary">Journal Entry</h4>
                    <p className="text-[12px] lg:text-[13px] text-on-surface-variant font-body-sm mt-1">Write your thoughts</p>
                  </div>
                </div>
              </Link>
            </div>

            <div className="grid grid-cols-2 gap-4 lg:gap-6 shrink-0">
              <div className="bg-white/50 backdrop-blur-xl border border-white shadow-sm rounded-[1.5rem] p-4 lg:p-6 flex flex-col justify-center items-center gap-2 hover:bg-white/80 transition-colors h-28 lg:h-32">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 lg:w-12 lg:h-12 rounded-full bg-primary/10 flex items-center justify-center mb-1">
                    <span className="material-symbols-outlined text-primary text-[20px] lg:text-[24px]" style={{ fontVariationSettings: "'FILL' 1" }}>local_fire_department</span>
                  </div>
                  <div className="flex flex-col">
                    <span className="text-display-sm font-headline-md text-primary text-2xl lg:text-3xl">5</span>
                    <span className="text-[10px] lg:text-xs text-on-surface-variant font-label-md uppercase tracking-wider leading-tight">Days<br/>Streak</span>
                  </div>
                </div>
              </div>
              <div className="bg-white/50 backdrop-blur-xl border border-white shadow-sm rounded-[1.5rem] p-4 lg:p-6 flex flex-col justify-center items-center gap-2 hover:bg-white/80 transition-colors h-28 lg:h-32">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 lg:w-12 lg:h-12 rounded-full bg-primary/10 flex items-center justify-center mb-1 relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-tr from-primary/30 to-tertiary/10 mix-blend-overlay"></div>
                    <span className="material-symbols-outlined text-primary text-[20px] lg:text-[24px]">waves</span>
                  </div>
                  <div className="flex flex-col gap-1">
                    <span className="text-display-sm font-headline-md text-primary text-xl lg:text-2xl">Balanced</span>
                    <span className="text-[9px] lg:text-[10px] text-on-surface-variant font-label-md uppercase tracking-wider">Weekly Mood</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="w-full bg-white/50 backdrop-blur-xl border border-white shadow-sm rounded-[2rem] p-6 lg:p-8 flex flex-col gap-4 lg:gap-6 flex-1 min-h-0">
              <div className="flex justify-between items-end">
                <div>
                  <h3 className="text-headline-md font-headline-md text-primary">Activity Trend</h3>
                  <p className="text-sm text-on-surface-variant mt-1">Sessions over the past 7 days</p>
                </div>
                <span className="text-primary bg-primary/10 px-4 py-1.5 rounded-full text-xs font-label-md uppercase tracking-wider">This Week</span>
              </div>
              <div className="flex justify-between items-end flex-1 pt-6 px-4">
                {[{h:'40%',l:'M'}, {h:'60%',l:'T'}, {h:'90%',l:'W',a:true}, {h:'30%',l:'T'}, {h:'75%',l:'F'}, {h:'15%',l:'S'}, {h:'20%',l:'S'}].map((bar, i) => (
                  <div key={i} className={`w-12 rounded-t-xl relative group transition-all ${bar.a ? 'bg-primary/70 hover:bg-primary/90 shadow-lg shadow-primary/20' : 'bg-primary/20 hover:bg-primary/40'}`} style={{ height: bar.h }}>
                    <span className={`absolute -top-7 left-1/2 -translate-x-1/2 text-xs ${bar.a ? 'font-bold text-primary opacity-100' : 'text-primary opacity-0 group-hover:opacity-100'} transition-opacity`}>{bar.l}</span>
                  </div>
                ))}
              </div>
              <div className="flex justify-between items-center px-4 text-xs font-label-md text-on-surface-variant/70 uppercase">
                {['M','T','W','T','F','S','S'].map((l, i) => (
                  <span key={i} className={`w-12 text-center ${i === 2 ? 'text-primary font-bold' : ''}`}>{l}</span>
                ))}
              </div>
            </div>
          </section>
        </div>
      </main>

      {/* Mobile Main Content */}
      <main className="flex md:hidden w-full max-w-[680px] mx-auto px-4 pb-28 pt-24 flex-col gap-5 overflow-y-auto z-10 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
        <section className="w-full bg-white/60 backdrop-blur-2xl border border-white border-b-primary/10 shadow-lg shadow-primary/5 rounded-3xl p-6 flex flex-col relative overflow-hidden transition-all duration-300 hover:shadow-xl">
          <div className="absolute -right-8 -top-8 w-32 h-32 bg-primary/10 rounded-full blur-2xl"></div>
          <h2 className="text-headline-sm font-headline-md text-primary mb-1">How are you feeling today?</h2>
          <p className="text-body-sm text-on-surface-variant mb-5">Take a moment to center yourself.</p>
          <div className="flex justify-between items-center gap-2">
            {['Calm', 'Focus', 'Anxious', 'Joyful'].map((mood, idx) => (
              <button key={mood} onClick={() => router.push('/consultation')} className="flex-1 flex flex-col items-center gap-2 p-3 rounded-2xl bg-white/50 border border-outline-variant/30 hover:bg-white/80 active:scale-95 transition-all">
                <span className="text-2xl">{['😌', '🎯', '💭', '✨'][idx]}</span>
                <span className="text-[11px] font-label-md text-primary uppercase tracking-wider">{mood}</span>
              </button>
            ))}
          </div>
        </section>

        <h3 className="text-label-md font-label-md text-on-surface-variant uppercase tracking-widest mt-2 px-1">Your Insights</h3>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-white/50 backdrop-blur-xl border border-white shadow-sm rounded-3xl p-5 flex flex-col justify-center items-center gap-1 hover:bg-white/70 transition-colors">
            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-1">
              <span className="material-symbols-outlined text-primary text-[24px]" style={{ fontVariationSettings: "'FILL' 1" }}>local_fire_department</span>
            </div>
            <span className="font-headline-md text-primary text-2xl">5 Days</span>
            <span className="text-[11px] text-on-surface-variant font-label-md uppercase tracking-wider">Current Streak</span>
          </div>
          <div className="bg-white/50 backdrop-blur-xl border border-white shadow-sm rounded-3xl p-5 flex flex-col justify-center items-center gap-1 hover:bg-white/70 transition-colors">
            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-1 relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-tr from-primary/30 to-tertiary/10 mix-blend-overlay"></div>
              <span className="material-symbols-outlined text-primary text-[24px]">waves</span>
            </div>
            <span className="font-headline-md text-primary text-2xl">Balanced</span>
            <span className="text-[11px] text-on-surface-variant font-label-md uppercase tracking-wider">Weekly Mood</span>
          </div>
        </div>

        <section className="w-full bg-white/50 backdrop-blur-xl border border-white shadow-sm rounded-3xl p-5 flex flex-col gap-4">
          <div className="flex justify-between items-end">
            <div>
              <h3 className="text-lg font-headline-md text-primary">Activity Trend</h3>
              <p className="text-[12px] text-on-surface-variant">Journaling &amp; Voice Sessions</p>
            </div>
            <span className="text-primary bg-primary/10 px-3 py-1 rounded-full text-[11px] font-label-md uppercase tracking-wider">This Week</span>
          </div>
          <div className="flex justify-between items-end h-24 pt-4 px-2">
            {[{h:'40%'}, {h:'60%'}, {h:'90%', a:true}, {h:'30%'}, {h:'75%'}, {h:'15%'}, {h:'20%'}].map((bar, i) => (
              <div key={i} className={`w-8 rounded-t-lg relative group transition-all ${bar.a ? 'bg-primary/70 hover:bg-primary/90' : 'bg-primary/20 hover:bg-primary/40'}`} style={{ height: bar.h }}></div>
            ))}
          </div>
          <div className="flex justify-between items-center px-2 text-[10px] font-label-md text-on-surface-variant/70 uppercase">
            <span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span><span>S</span>
          </div>
        </section>

        <h3 className="text-label-md font-label-md text-on-surface-variant uppercase tracking-widest mt-2 px-1">Quick Actions</h3>
        <div className="flex flex-col gap-3 mb-4">
          <Link href="/voice" className="w-full bg-plum-high-contrast text-white p-4 rounded-3xl flex items-center justify-between shadow-lg shadow-plum-high-contrast/20 hover:opacity-95 active:scale-[0.98] transition-all">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center backdrop-blur-md">
                <span className="material-symbols-outlined text-[24px]">mic</span>
              </div>
              <div>
                <h4 className="font-headline-md text-lg">Start Voice Session</h4>
                <p className="text-[12px] opacity-80 font-body-sm">Speak your mind freely</p>
              </div>
            </div>
            <span className="material-symbols-outlined">arrow_forward_ios</span>
          </Link>
          <Link href="/history" className="w-full bg-white/60 backdrop-blur-xl border border-white p-4 rounded-3xl flex items-center justify-between shadow-sm hover:bg-white/80 active:scale-[0.98] transition-all">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                <span className="material-symbols-outlined text-[24px] text-primary">edit_document</span>
              </div>
              <div>
                <h4 className="font-headline-md text-lg text-primary">New Journal Entry</h4>
                <p className="text-[12px] text-on-surface-variant font-body-sm">Write down your thoughts</p>
              </div>
            </div>
            <span className="material-symbols-outlined text-primary">arrow_forward_ios</span>
          </Link>
        </div>
      </main>

    </>
  )
}

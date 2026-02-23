import React, { useState, useEffect } from 'react';
import { ArrowLeft, Users, Briefcase, Award, Zap, DollarSign, Activity } from 'lucide-react';

const StaffMarket = ({ gameState, onNavigate, refreshState }) => {
    const [market, setMarket] = useState(null);
    const [activeTab, setActiveTab] = useState('drivers'); // 'drivers', 'technical_directors', 'head_of_aero', 'powertrain_leads'
    const [loading, setLoading] = useState(false);
    const [selectedSlot, setSelectedSlot] = useState(null); // Used for drivers when hiring
    const [pendingHire, setPendingHire] = useState(null); // Which staff member is queued for hire

    useEffect(() => {
        const fetchMarket = async () => {
            try {
                const res = await fetch('http://localhost:8000/api/staff/market');
                const data = await res.json();
                setMarket(data.market);
            } catch (err) {
                console.error("Failed to fetch market:", err);
            }
        };
        fetchMarket();
    }, []);

    const { finance_manager } = gameState;

    const handleHire = async (staffId, slotId) => {
        setLoading(true);
        try {
            const res = await fetch('http://localhost:8000/api/staff/hire', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slot: slotId, staff_id: staffId })
            });
            const data = await res.json();
            if (data.status === 'success') {
                await refreshState();
                const freshMarket = await fetch('http://localhost:8000/api/staff/market').then(r => r.json());
                setMarket(freshMarket.market);
                setPendingHire(null);
                setSelectedSlot(null);
            } else {
                alert(data.detail || "Failed to hire staff.");
            }
        } catch (e) {
            console.error(e);
        }
        setLoading(false);
    };

    const handleFire = async (slotId) => {
        setLoading(true);
        try {
            const res = await fetch('http://localhost:8000/api/staff/fire', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slot: slotId })
            });
            const data = await res.json();
            if (data.status === 'success') {
                await refreshState();
                const freshMarket = await fetch('http://localhost:8000/api/staff/market').then(r => r.json());
                setMarket(freshMarket.market);
            } else {
                alert(data.detail || "Failed to fire staff.");
            }
        } catch (e) {
            console.error(e);
        }
        setLoading(false);
    };

    if (!market) {
        return <div className="p-8 text-center text-slate-400 animate-pulse">Loading Free Agent Database...</div>;
    }

    const tabs = [
        { id: 'drivers', label: 'Drivers', icon: Users, defaultSlot: 'driver_0' },
        { id: 'technical_directors', label: 'Technical Director', icon: Briefcase, defaultSlot: 'technical_director' },
        { id: 'head_of_aero', label: 'Head of Aero', icon: Zap, defaultSlot: 'head_of_aero' },
        { id: 'powertrain_leads', label: 'Powertrain Lead', icon: Activity, defaultSlot: 'powertrain_lead' }
    ];

    const getActiveStaffForTab = () => {
        if (activeTab === 'drivers') return gameState.drivers;
        if (activeTab === 'technical_directors') return gameState.technical_director ? [gameState.technical_director] : [];
        if (activeTab === 'head_of_aero') return gameState.head_of_aero ? [gameState.head_of_aero] : [];
        if (activeTab === 'powertrain_leads') return gameState.powertrain_lead ? [gameState.powertrain_lead] : [];
        return [];
    };

    const renderStaffStats = (staff) => {
        if (activeTab === 'drivers') {
            return (
                <div className="grid grid-cols-2 gap-2 text-xs text-slate-400 mt-2">
                    <div>Pace: <span className="text-white font-bold">{staff.pace}</span></div>
                    <div>Consistency: <span className="text-white font-bold">{staff.consistency}</span></div>
                    <div>Experience: <span className="text-white font-bold">{staff.experience}</span></div>
                    <div>Racecraft: <span className="text-white font-bold">{staff.racecraft}</span></div>
                </div>
            );
        } else if (activeTab === 'technical_directors') {
            return (
                <div className="grid grid-cols-2 gap-2 text-xs text-slate-400 mt-2">
                    <div>Leadership: <span className="text-white font-bold">{staff.leadership}</span></div>
                </div>
            );
        } else {
            return (
                <div className="grid grid-cols-2 gap-2 text-xs text-slate-400 mt-2">
                    <div>Expertise: <span className="text-white font-bold">{staff.expertise}</span></div>
                    <div>Leadership: <span className="text-white font-bold">{staff.leadership}</span></div>
                </div>
            );
        }
    };

    const renderStaffCard = (staff, isActive, slotId = null) => {
        if (!staff) return (
            <div className="bg-slate-800/30 border border-slate-700 border-dashed rounded-xl p-6 flex flex-col items-center justify-center text-slate-500 min-h-[150px]">
                <span className="italic">Vacant Position</span>
            </div>
        );

        return (
            <div className={`bg-slate-800 rounded-xl p-5 border ${isActive ? 'border-f1accent shadow-lg shadow-blue-500/10' : 'border-slate-700'}`}>
                <div className="flex justify-between items-start mb-3">
                    <div>
                        <h3 className="font-bold text-lg text-white">{staff.name}</h3>
                        <p className="text-xs text-slate-400">Age {staff.age} • {staff.contract_length_years} Year Contract</p>
                    </div>
                    <div className="bg-slate-900 border border-slate-600 px-3 py-1 text-xl font-black text-f1accent rounded shadow-inner">
                        {staff.rating}
                    </div>
                </div>

                <div className="flex items-center gap-1 text-sm text-f1green font-mono mb-3 bg-slate-900/50 p-2 rounded">
                    <DollarSign size={14} /> {(staff.salary / 1000000).toFixed(1)}M / Season
                </div>

                {renderStaffStats(staff)}

                <div className="mt-4 pt-4 border-t border-slate-700/50">
                    {isActive ? (
                        activeTab !== 'drivers' ? (
                            <button
                                onClick={() => handleFire(slotId)}
                                disabled={loading}
                                className="w-full py-2 bg-red-900/20 hover:bg-red-900/40 text-red-500 border border-red-900 rounded font-bold text-sm transition-colors"
                            >
                                Fire (Severance: ${((staff.salary * staff.contract_length_years * 0.5) / 1000000).toFixed(1)}M)
                            </button>
                        ) : (
                            <div className="text-center text-xs text-slate-500 italic py-1">Must hire replacement to fire driver.</div>
                        )
                    ) : (
                        <button
                            onClick={() => {
                                if (activeTab === 'drivers') {
                                    setPendingHire(staff);
                                } else {
                                    handleHire(staff.id, tabs.find(t => t.id === activeTab).defaultSlot);
                                }
                            }}
                            disabled={loading || (finance_manager.balance < staff.salary * 0.5)}
                            className="w-full py-2 bg-f1green/20 hover:bg-f1green/40 text-f1green border border-f1green/50 rounded font-bold text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Hire (Sign Bonus: ${((staff.salary * 0.5) / 1000000).toFixed(1)}M)
                        </button>
                    )}
                </div>
            </div>
        );
    };

    return (
        <div className="flex flex-col h-full bg-slate-900">
            {/* Header */}
            <div className="bg-f1panel px-8 py-5 flex items-center justify-between border-b border-slate-800 shrink-0 shadow-md z-10">
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => onNavigate('dashboard')}
                        className="bg-slate-800 hover:bg-slate-700 text-slate-300 p-2 rounded-full transition-colors"
                    >
                        <ArrowLeft size={20} />
                    </button>
                    <div>
                        <h2 className="text-2xl font-black text-white uppercase tracking-tight">Staff Market</h2>
                        <p className="text-slate-400 text-sm">Scout and manage your organization's personnel.</p>
                    </div>
                </div>

                <div className="bg-slate-800 px-6 py-3 rounded border border-slate-700 flex flex-col items-end shadow-inner">
                    <span className="text-xs text-slate-400 font-bold uppercase tracking-widest">Available Budget</span>
                    <span className="text-xl font-bold text-f1green font-mono">${(finance_manager.balance / 1000000).toFixed(2)}M</span>
                </div>
            </div>

            {/* Content Area */}
            <div className="flex flex-1 overflow-hidden">
                {/* Left Sidebar - Tabs */}
                <div className="w-64 bg-slate-900 border-r border-slate-800 p-4 shrink-0 overflow-y-auto">
                    <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4 px-2">Departments</h3>
                    <div className="space-y-2">
                        {tabs.map(tab => (
                            <button
                                key={tab.id}
                                onClick={() => { setActiveTab(tab.id); setPendingHire(null); }}
                                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-bold transition-all
                                    ${activeTab === tab.id
                                        ? 'bg-f1accent text-slate-900 shadow-md shadow-blue-900/20'
                                        : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                                    }`}
                            >
                                <tab.icon size={18} />
                                {tab.label}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Main Market View */}
                <div className="flex-1 overflow-y-auto p-8 relative">

                    {/* Hire Driver Modal / Overlay */}
                    {pendingHire && activeTab === 'drivers' && (
                        <div className="absolute inset-0 bg-slate-900/90 backdrop-blur-sm z-20 flex items-center justify-center p-8">
                            <div className="bg-f1panel border border-slate-700 rounded-xl p-8 max-w-xl w-full shadow-2xl">
                                <h3 className="text-2xl font-bold text-white mb-2">Hire {pendingHire.name}?</h3>
                                <p className="text-slate-400 text-sm mb-6">Select which current driver you wish to terminate to make room for {pendingHire.name}. You will be charged their signing bonus, plus the severance package of the driver you fire.</p>

                                <div className="grid grid-cols-2 gap-4 mb-6">
                                    <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
                                        <p className="text-xs text-slate-500 font-bold uppercase mb-2">Driver 1 (Car 1)</p>
                                        <p className="font-bold text-white mb-1">{gameState.drivers[0].name}</p>
                                        <p className="text-xs text-f1accent mb-4">OVR {gameState.drivers[0].rating}</p>
                                        <button
                                            onClick={() => handleHire(pendingHire.id, 'driver_0')}
                                            className="w-full bg-red-900/30 hover:bg-red-500 text-white font-bold py-2 rounded text-sm transition-colors border border-red-900"
                                        >
                                            Replace (-${(((pendingHire.salary * 0.5) + (gameState.drivers[0].salary * gameState.drivers[0].contract_length_years * 0.5)) / 1000000).toFixed(1)}M)
                                        </button>
                                    </div>
                                    <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
                                        <p className="text-xs text-slate-500 font-bold uppercase mb-2">Driver 2 (Car 2)</p>
                                        <p className="font-bold text-white mb-1">{gameState.drivers[1].name}</p>
                                        <p className="text-xs text-f1accent mb-4">OVR {gameState.drivers[1].rating}</p>
                                        <button
                                            onClick={() => handleHire(pendingHire.id, 'driver_1')}
                                            className="w-full bg-red-900/30 hover:bg-red-500 text-white font-bold py-2 rounded text-sm transition-colors border border-red-900"
                                        >
                                            Replace (-${(((pendingHire.salary * 0.5) + (gameState.drivers[1].salary * gameState.drivers[1].contract_length_years * 0.5)) / 1000000).toFixed(1)}M)
                                        </button>
                                    </div>
                                </div>
                                <button
                                    onClick={() => setPendingHire(null)}
                                    className="w-full text-center text-slate-400 hover:text-white text-sm"
                                >
                                    Cancel
                                </button>
                            </div>
                        </div>
                    )}


                    <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
                        {/* Active Staff Column */}
                        <div className="xl:col-span-4 flex flex-col gap-4">
                            <h3 className="text-sm font-bold text-white uppercase tracking-widest border-b border-slate-800 pb-2 flex items-center gap-2">
                                <Award size={16} className="text-f1accent" /> Current {tabs.find(t => t.id === activeTab).label}
                            </h3>
                            <div className="space-y-4">
                                {activeTab === 'drivers' ? (
                                    <>
                                        {renderStaffCard(gameState.drivers[0], true, 'driver_0')}
                                        {renderStaffCard(gameState.drivers[1], true, 'driver_1')}
                                    </>
                                ) : (
                                    renderStaffCard(getActiveStaffForTab()[0], true, tabs.find(t => t.id === activeTab).defaultSlot)
                                )}
                            </div>
                        </div>

                        {/* Free Agents Column */}
                        <div className="xl:col-span-8 flex flex-col gap-4">
                            <h3 className="text-sm font-bold text-white uppercase tracking-widest border-b border-slate-800 pb-2 flex items-center gap-2">
                                <Users size={16} className="text-slate-400" /> Free Agents Market
                            </h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {market[activeTab] && market[activeTab].length > 0 ? (
                                    market[activeTab].map(staff => (
                                        <div key={staff.id}>
                                            {renderStaffCard(staff, false)}
                                        </div>
                                    ))
                                ) : (
                                    <div className="col-span-2 py-12 text-center text-slate-500 italic bg-slate-800/20 rounded-xl border border-slate-800">
                                        No free agents currently available in the market.
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default StaffMarket;

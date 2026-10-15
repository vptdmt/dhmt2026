import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('index_template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ================================================================
# SECTION 1: GLOBAL TOURNAMENT ENGINE & LIVE SYNC CORE
# Placed right before TAB SWITCHING
# ================================================================
core_engine_code = '''// ================================================================
// LIVE TOURNAMENT BRACKET & SCHEDULE SYNCHRONIZATION ENGINE
// ================================================================
let tourScores = JSON.parse(localStorage.getItem('dhmt2026_scores') || '{}');

function saveTourScores() {
  localStorage.setItem('dhmt2026_scores', JSON.stringify(tourScores));
}

// Helper to determine winner and loser from scores
function getWinnerAndLoser(m, scoreObj) {
  if (!scoreObj || scoreObj.s1 === null || scoreObj.s1 === undefined || scoreObj.s2 === null || scoreObj.s2 === undefined) {
    return { winner: null, loser: null, isDecided: false };
  }
  const s1 = Number(scoreObj.s1);
  const s2 = Number(scoreObj.s2);
  if (isNaN(s1) || isNaN(s2)) return { winner: null, loser: null, isDecided: false };
  if (s1 > s2) {
    return { winner: m.team1, loser: m.team2, isDecided: true, winIdx: 1 };
  } else if (s2 > s1) {
    return { winner: m.team2, loser: m.team1, isDecided: true, winIdx: 2 };
  }
  return { winner: null, loser: null, isDecided: false };
}

// Group Standings Calculator (Used by Kéo co, Bóng đá Nữ, Cầu lông Đôi Nam-Nữ, Bóng bàn)
function computeGroupStandings(group, tourId, isFootball = false) {
  const standings = group.teams.map(t => ({
    id: t.id,
    code: t.code,
    name: t.name,
    sub: t.sub || '',
    played: 0,
    won: 0,
    drawn: 0,
    lost: 0,
    gf: 0, // Goals for or Sets won
    ga: 0, // Goals against or Sets lost
    gd: 0, // Goal / Set diff
    points: 0
  }));

  const matches = group.matches || [];
  matches.forEach(m => {
    const scores = (tourScores[tourId] && tourScores[tourId][m.id]) || {};
    if (scores.s1 !== null && scores.s1 !== undefined && scores.s2 !== null && scores.s2 !== undefined) {
      const s1 = Number(scores.s1);
      const s2 = Number(scores.s2);
      
      const t1 = standings.find(x => x.id === m.team1);
      const t2 = standings.find(x => x.id === m.team2);
      
      if (t1 && t2) {
        t1.played++;
        t2.played++;
        t1.gf += s1;
        t1.ga += s2;
        t2.gf += s2;
        t2.ga += s1;
        
        if (s1 > s2) {
          t1.won++;
          t1.points += isFootball ? 3 : 2;
          t2.lost++;
        } else if (s2 > s1) {
          t2.won++;
          t2.points += isFootball ? 3 : 2;
          t1.lost++;
        } else {
          t1.drawn++;
          t2.drawn++;
          t1.points += 1;
          t2.points += 1;
        }
      }
    }
  });

  standings.forEach(t => { t.gd = t.gf - t.ga; });

  // Sort by Points desc, then Diff desc, then GF desc
  standings.sort((a, b) => {
    if (b.points !== a.points) return b.points - a.points;
    if (b.gd !== a.gd) return b.gd - a.gd;
    return b.gf - a.gf;
  });

  return standings;
}

// Master Live State Progression: updates live teams for ALL tournaments based on scores
function updateAllTournamentsLiveState() {
  const tournaments = DATA.tournaments || [];
  tournaments.forEach(tour => {
    const tScores = tourScores[tour.id] || {};

    if (tour.format === 'knockout8') {
      const roundTK = tour.rounds.find(r => r.id === 'tk');
      const roundBK = tour.rounds.find(r => r.id === 'bk');
      const roundFN = tour.rounds.find(r => r.id === 'fn');
      if (!roundTK || !roundBK || !roundFN) return;
      
      // Progression 1: Winners of TK -> BK
      const tkWinners = roundTK.matches.map(m => getWinnerAndLoser(m, tScores[m.id] || {}).winner);
      
      roundBK.matches[0].team1 = tkWinners[0] || { name: 'Thắng TK1', isPlaceholder: true };
      roundBK.matches[0].team2 = tkWinners[1] || { name: 'Thắng TK2', isPlaceholder: true };
      roundBK.matches[1].team1 = tkWinners[2] || { name: 'Thắng TK3', isPlaceholder: true };
      roundBK.matches[1].team2 = tkWinners[3] || { name: 'Thắng TK4', isPlaceholder: true };
      
      // Progression 2: Winners & Losers of BK -> Finals & 3rd Place
      const bkRes0 = getWinnerAndLoser(roundBK.matches[0], tScores[roundBK.matches[0].id] || {});
      const bkRes1 = getWinnerAndLoser(roundBK.matches[1], tScores[roundBK.matches[1].id] || {});
      
      const mCK = roundFN.matches.find(m => m.isFinal || m.id.endsWith('CK'));
      const m34 = roundFN.matches.find(m => m.isThirdPlace || m.id.includes('3-4') || m.id.includes('Ba-Tư'));
      
      if (mCK) {
        mCK.team1 = bkRes0.winner || { name: 'Thắng BK1', isPlaceholder: true };
        mCK.team2 = bkRes1.winner || { name: 'Thắng BK2', isPlaceholder: true };
      }
      if (m34) {
        m34.team1 = bkRes0.loser || { name: 'Thua BK1', isPlaceholder: true };
        m34.team2 = bkRes1.loser || { name: 'Thua BK2', isPlaceholder: true };
      }
    } else if (tour.format === 'group2_cross') {
      const grpA = tour.groups[0];
      const grpB = tour.groups[1];
      const stdA = computeGroupStandings(grpA, tour.id, false);
      const stdB = computeGroupStandings(grpB, tour.id, false);
      const isAStarted = stdA.some(t => t.played > 0);
      const isBStarted = stdB.some(t => t.played > 0);
      
      const roundBK = tour.knockout.find(r => r.id === 'bk');
      const roundFN = tour.knockout.find(r => r.id === 'fn');
      if (!roundBK || !roundFN) return;
      
      roundBK.matches[0].team1 = isAStarted ? { code: '1A', name: stdA[0].name, sub: 'Nhất Bảng A' } : { code: '1A', name: 'Nhất Bảng A', isPlaceholder: true };
      roundBK.matches[0].team2 = isBStarted ? { code: '2B', name: stdB[1].name, sub: 'Nhì Bảng B' } : { code: '2B', name: 'Nhì Bảng B', isPlaceholder: true };
      roundBK.matches[1].team1 = isBStarted ? { code: '1B', name: stdB[0].name, sub: 'Nhất Bảng B' } : { code: '1B', name: 'Nhất Bảng B', isPlaceholder: true };
      roundBK.matches[1].team2 = isAStarted ? { code: '2A', name: stdA[1].name, sub: 'Nhì Bảng A' } : { code: '2A', name: 'Nhì Bảng A', isPlaceholder: true };
      
      const bkRes0 = getWinnerAndLoser(roundBK.matches[0], tScores[roundBK.matches[0].id] || {});
      const bkRes1 = getWinnerAndLoser(roundBK.matches[1], tScores[roundBK.matches[1].id] || {});
      
      const mCK = roundFN.matches.find(m => m.isFinal || m.id.endsWith('CK'));
      const m34 = roundFN.matches.find(m => m.isThirdPlace || m.id.includes('3-4'));
      if (mCK) {
        mCK.team1 = bkRes0.winner || { name: 'Thắng BK1', isPlaceholder: true };
        mCK.team2 = bkRes1.winner || { name: 'Thắng BK2', isPlaceholder: true };
      }
      if (m34) {
        m34.team1 = bkRes0.loser || { name: 'Thua BK1', isPlaceholder: true };
        m34.team2 = bkRes1.loser || { name: 'Thua BK2', isPlaceholder: true };
      }
    } else if (tour.format === 'group2_final') {
      const grpA = tour.groups[0];
      const grpB = tour.groups[1];
      const stdA = computeGroupStandings(grpA, tour.id, true);
      const stdB = computeGroupStandings(grpB, tour.id, true);
      const isAStarted = stdA.some(t => t.played > 0);
      const isBStarted = stdB.some(t => t.played > 0);
      
      const mCK = tour.finals.find(m => m.isFinal || m.id.endsWith('CK'));
      const m34 = tour.finals.find(m => m.isThirdPlace || m.id.includes('3-4'));
      if (mCK) {
        mCK.team1 = isAStarted ? { code: '1A', name: stdA[0].name, sub: 'Nhất Bảng A' } : { code: '1A', name: 'Nhất Bảng A', isPlaceholder: true };
        mCK.team2 = isBStarted ? { code: '1B', name: stdB[0].name, sub: 'Nhất Bảng B' } : { code: '1B', name: 'Nhất Bảng B', isPlaceholder: true };
      }
      if (m34) {
        m34.team1 = isAStarted ? { code: '2A', name: stdA[1].name, sub: 'Nhì Bảng A' } : { code: '2A', name: 'Nhì Bảng A', isPlaceholder: true };
        m34.team2 = isBStarted ? { code: '2B', name: stdB[1].name, sub: 'Nhì Bảng B' } : { code: '2B', name: 'Nhì Bảng B', isPlaceholder: true };
      }
    } else if (tour.format === 'tabletennis_men') {
      const po1 = tour.playoffs[0];
      const po2 = tour.playoffs[1];
      const po1Res = getWinnerAndLoser(po1, tScores[po1.id] || {});
      const po2Res = getWinnerAndLoser(po2, tScores[po2.id] || {});
      
      const grpA = tour.groups[0];
      const grpB = tour.groups[1];
      grpA.teams[0].name = po2Res.winner ? po2Res.winner.name : 'Thắng PO2 (Tuấn / Trạng)';
      grpA.teams[0].code = po2Res.winner ? po2Res.winner.code : 'PO2';
      grpB.teams[0].name = po1Res.winner ? po1Res.winner.name : 'Thắng PO1 (Hùng / Phú)';
      grpB.teams[0].code = po1Res.winner ? po1Res.winner.code : 'PO1';
      
      const stdA = computeGroupStandings(grpA, tour.id, false);
      const stdB = computeGroupStandings(grpB, tour.id, false);
      const isAStarted = stdA.some(t => t.played > 0);
      const isBStarted = stdB.some(t => t.played > 0);
      
      const roundBK = tour.knockout.find(r => r.id === 'bk');
      const roundFN = tour.knockout.find(r => r.id === 'fn');
      if (!roundBK || !roundFN) return;
      
      roundBK.matches[0].team1 = isAStarted ? { code: '1A', name: stdA[0].name, sub: 'Nhất Bảng A' } : { code: '1A', name: 'Nhất Bảng A', isPlaceholder: true };
      roundBK.matches[0].team2 = isBStarted ? { code: '2B', name: stdB[1].name, sub: 'Nhì Bảng B' } : { code: '2B', name: 'Nhì Bảng B', isPlaceholder: true };
      roundBK.matches[1].team1 = isBStarted ? { code: '1B', name: stdB[0].name, sub: 'Nhất Bảng B' } : { code: '1B', name: 'Nhất Bảng B', isPlaceholder: true };
      roundBK.matches[1].team2 = isAStarted ? { code: '2A', name: stdA[1].name, sub: 'Nhì Bảng A' } : { code: '2A', name: 'Nhì Bảng A', isPlaceholder: true };
      
      const bkRes0 = getWinnerAndLoser(roundBK.matches[0], tScores[roundBK.matches[0].id] || {});
      const bkRes1 = getWinnerAndLoser(roundBK.matches[1], tScores[roundBK.matches[1].id] || {});
      
      const mCK = roundFN.matches.find(m => m.isFinal || m.id.endsWith('CK'));
      const m34 = roundFN.matches.find(m => m.isThirdPlace || m.id.includes('Ba-Tư'));
      if (mCK) {
        mCK.team1 = bkRes0.winner || { name: 'Thắng BK1', isPlaceholder: true };
        mCK.team2 = bkRes1.winner || { name: 'Thắng BK2', isPlaceholder: true };
      }
      if (m34) {
        m34.team1 = bkRes0.loser || { name: 'Thua BK1', isPlaceholder: true };
        m34.team2 = bkRes1.loser || { name: 'Thua BK2', isPlaceholder: true };
      }
    } else if (tour.format === 'group3_roundrobin') {
      const grps = tour.groups;
      const stds = grps.map(g => computeGroupStandings(g, tour.id, false));
      const finalMatches = tour.finalRound.matches;
      const isAStarted = stds[0].some(t => t.played > 0);
      const isBStarted = stds[1].some(t => t.played > 0);
      const isCStarted = stds[2].some(t => t.played > 0);
      
      finalMatches[0].team1 = isAStarted ? { code: '1A', name: stds[0][0].name, sub: 'Nhất Bảng A' } : { code: '1A', name: 'Nhất Bảng A', isPlaceholder: true };
      finalMatches[0].team2 = isBStarted ? { code: '1B', name: stds[1][0].name, sub: 'Nhất Bảng B' } : { code: '1B', name: 'Nhất Bảng B', isPlaceholder: true };
      finalMatches[1].team1 = isBStarted ? { code: '1B', name: stds[1][0].name, sub: 'Nhất Bảng B' } : { code: '1B', name: 'Nhất Bảng B', isPlaceholder: true };
      finalMatches[1].team2 = isCStarted ? { code: '1C', name: stds[2][0].name, sub: 'Nhất Bảng C' } : { code: '1C', name: 'Nhất Bảng C', isPlaceholder: true };
      finalMatches[2].team1 = isCStarted ? { code: '1C', name: stds[2][0].name, sub: 'Nhất Bảng C' } : { code: '1C', name: 'Nhất Bảng C', isPlaceholder: true };
      finalMatches[2].team2 = isAStarted ? { code: '1A', name: stds[0][0].name, sub: 'Nhất Bảng A' } : { code: '1A', name: 'Nhất Bảng A', isPlaceholder: true };
    }
  });
}

// Find matching tournament and match for any schedule cell
function findMatchForScheduleCell(cell) {
  if (!cell || !cell.noiDung) return null;
  const noiDung = cell.noiDung;
  const tournaments = DATA.tournaments || [];
  
  for (const tour of tournaments) {
    let allMatches = [];
    if (tour.format === 'knockout8') {
      tour.rounds.forEach(r => r.matches.forEach(m => allMatches.push(m)));
    } else if (tour.format === 'group2_cross' || tour.format === 'tabletennis_men') {
      if (tour.playoffs) tour.playoffs.forEach(m => allMatches.push(m));
      tour.groups.forEach(g => {
        g.matches.forEach(m => {
          const t1 = g.teams.find(x => x.id === m.team1) || { name: m.team1 };
          const t2 = g.teams.find(x => x.id === m.team2) || { name: m.team2 };
          allMatches.push({ ...m, team1: t1, team2: t2 });
        });
      });
      tour.knockout.forEach(r => r.matches.forEach(m => allMatches.push(m)));
    } else if (tour.format === 'group2_final') {
      tour.groups.forEach(g => {
        g.matches.forEach(m => {
          const t1 = g.teams.find(x => x.id === m.team1) || { name: m.team1 };
          const t2 = g.teams.find(x => x.id === m.team2) || { name: m.team2 };
          allMatches.push({ ...m, team1: t1, team2: t2 });
        });
      });
      tour.finals.forEach(m => allMatches.push(m));
    } else if (tour.format === 'group3_roundrobin') {
      tour.groups.forEach(g => {
        g.matches.forEach(m => {
          const t1 = g.teams.find(x => x.id === m.team1) || { name: m.team1 };
          const t2 = g.teams.find(x => x.id === m.team2) || { name: m.team2 };
          allMatches.push({ ...m, team1: t1, team2: t2 });
        });
      });
      if (tour.finalRound) tour.finalRound.matches.forEach(m => allMatches.push(m));
    }

    for (const m of allMatches) {
      let isMatch = false;
      const mId = m.id;
      
      if (noiDung.includes(mId)) isMatch = true;
      else if (noiDung.includes(mId.replace('BD.', 'BĐ.'))) isMatch = true;
      else if (noiDung.includes(mId.replace('BĐ.', 'BD.'))) isMatch = true;
      // Special variations:
      else if (tour.id === 'kc' && mId === 'KC.CK' && noiDung.includes('KC.Chung kết')) isMatch = true;
      else if (tour.id === 'kc' && mId === 'KC.3-4' && (noiDung.includes('KC.Tranh 3-4') || noiDung.includes('KC.3-4'))) isMatch = true;
      else if (tour.id === 'cl_mf' && mId === 'CL.MF.F1' && noiDung.includes('Nhất A-Nhất B')) isMatch = true;
      else if (tour.id === 'cl_mf' && mId === 'CL.MF.F2' && noiDung.includes('Nhất B-Nhất C')) isMatch = true;
      else if (tour.id === 'cl_mf' && mId === 'CL.MF.F3' && noiDung.includes('Nhất C-Nhất A')) isMatch = true;
      else if (tour.id === 'bb_f' && mId === 'BB.F.F1' && noiDung.includes('Nhất A-Nhất B')) isMatch = true;
      else if (tour.id === 'bb_f' && mId === 'BB.F.F2' && noiDung.includes('Nhất B-Nhất C')) isMatch = true;
      else if (tour.id === 'bb_f' && mId === 'BB.F.F3' && noiDung.includes('Nhất C-Nhất A')) isMatch = true;

      if (isMatch) {
        const sc = (tourScores[tour.id] && tourScores[tour.id][m.id]) || {};
        const hasScore = sc.s1 !== null && sc.s1 !== undefined && sc.s2 !== null && sc.s2 !== undefined && sc.s1 !== '' && sc.s2 !== '';
        const res = getWinnerAndLoser(m, sc);
        const hasLiveTeams = m.team1 && !m.team1.isPlaceholder && m.team2 && !m.team2.isPlaceholder;
        
        return {
          found: true,
          tour,
          match: m,
          matchCode: m.id.replace('BD.', 'BĐ.'),
          hasLiveTeams,
          team1: m.team1,
          team2: m.team2,
          scores: sc,
          hasScore,
          isDecided: res.isDecided,
          winner: res.winner,
          loser: res.loser
        };
      }
    }
  }
  return null;
}

// Find squad athletes for a team in tournament
function findAthletesForTeam(team, sport) {
  if (!team || team.isPlaceholder) return [];
  const keys = typeof team === 'object' 
    ? [team.code, team.name, team.sub, team.id].filter(Boolean)
    : [team];
  
  const units = DATA.sportUnits || [];
  for (const k of keys) {
    const cleanK = k.toLowerCase().replace('lq.', '').trim();
    for (const u of units) {
      if (sport && u.mon && !u.mon.toLowerCase().includes(sport.toLowerCase()) && !sport.toLowerCase().includes(u.mon.toLowerCase())) continue;
      const uSub = (u.sub || '').toLowerCase().replace('lq.', '');
      const uCode = (u.code || '').toLowerCase().replace('lq.', '');
      const aliases = (u.aliases || []).map(a => a.toLowerCase().replace('lq.', ''));
      if (aliases.includes(cleanK) || uSub.includes(cleanK) || uCode.includes(cleanK) || cleanK.includes(uSub)) {
        return u.athletes || [];
      }
    }
  }

  // Bracket names for pairs (e.g. Vinh - Chí)
  for (const k of keys) {
    if (k.includes('-') || k.includes('–')) {
      const names = k.replace(/[()]/g, '').split(/[-–]/).map(n => n.trim().toLowerCase()).filter(Boolean);
      for (const u of units) {
        if (u.bracketNames && u.bracketNames.length === names.length) {
          if (names.every(n => u.bracketNames.includes(n))) {
            return u.athletes || [];
          }
        }
      }
    }
  }

  // Exact name matches from DATA.athletes for single players
  for (const k of keys) {
    const cleanK = k.trim().toLowerCase();
    const exactMatches = (DATA.athletes || []).filter(a => a.hoVaTen.toLowerCase() === cleanK);
    if (exactMatches.length > 0) return exactMatches;
  }

  return [];
}

// Quick jump to tournament tab and select specific sport
function switchToTournamentTab(tourId, matchId) {
  closeModal();
  switchTab('results');
  if (tourId) {
    currentTourId = tourId;
    currentTourSportFilter = 'all';
    populateTournamentSelect();
    renderTournamentView();
    
    // Smooth scroll to tournament view container
    setTimeout(() => {
      const container = document.getElementById('tournament-view-container');
      if (container) container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 150);
  }
}
'''

# Check where to insert core_engine_code
# Right before `// TAB SWITCHING`
tab_switch_marker = '// ================================================================\n// TAB SWITCHING'
if tab_switch_marker in content:
    content = content.replace(tab_switch_marker, core_engine_code + '\n' + tab_switch_marker)
    print("Injected core tournament engine above TAB SWITCHING.")
else:
    print("Error: TAB SWITCHING marker not found!")
    sys.exit(1)

# ================================================================
# SECTION 2: UPDATE switchTab to safely handle missing btn
# ================================================================
old_switch_tab = '''function switchTab(name, btn) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
  const target = document.getElementById('tab-' + name);
  target.classList.remove('hidden');
  target.classList.add('slide-in');
  
  if (name === 'agenda') renderAgenda();
  else if (name === 'schedule') renderSchedule();
  else if (name === 'athletes') filterAthletes();
  else if (name === 'venues') renderVenuesTab();
  else if (name === 'results') renderResults();
}'''

new_switch_tab = '''function switchTab(name, btn) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  if (btn) {
    btn.classList.add('active');
  } else {
    const b = document.querySelector(`.tab-btn[data-tab="${name}"]`);
    if (b) b.classList.add('active');
  }
  document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
  const target = document.getElementById('tab-' + name);
  if (target) {
    target.classList.remove('hidden');
    target.classList.add('slide-in');
  }
  
  if (name === 'agenda') renderAgenda();
  else if (name === 'schedule') renderSchedule();
  else if (name === 'athletes') filterAthletes();
  else if (name === 'venues') renderVenuesTab();
  else if (name === 'results') renderResults();
}'''

if old_switch_tab in content:
    content = content.replace(old_switch_tab, new_switch_tab)
    print("Updated switchTab safely.")
else:
    print("Warning: old_switch_tab not found, trying regex...")

# ================================================================
# SECTION 3: UPDATE Tab 2 renderSchedule() and showScheduleDetail()
# ================================================================
old_render_schedule = '''function renderSchedule() {
  const monF = document.getElementById('filter-mon-sch').value;
  const sanF = document.getElementById('filter-san-sch').value;
  const q = (document.getElementById('search-team').value || '').trim().toLowerCase();
  
  let rows = DATA.schedule.filter(s => s.ngay === currentDay);
  if (monF) rows = rows.filter(s => s.mon === monF);
  if (sanF) rows = rows.filter(s => s.san === sanF);
  if (q) rows = rows.filter(s => s.noiDung.toLowerCase().includes(q) || s.san.toLowerCase().includes(q) || s.mon.toLowerCase().includes(q));
  
  document.getElementById('sch-count').textContent = rows.length + ' trận/ô lịch';
  
  if (!rows.length) {
    document.getElementById('schedule-grid').innerHTML = `
      <div class="p-12 text-center text-slate-400">
        <div class="text-4xl mb-2">📋</div>
        <p class="font-bold text-sm text-slate-600">Không có lịch thi đấu phù hợp với bộ lọc</p>
        <p class="text-xs text-slate-400 mt-1">Hãy thử chọn ngày khác hoặc bỏ bớt tiêu chí lọc</p>
      </div>`;
    return;
  }

  const timeSlots = [...new Set(rows.map(s => s.batdau))].sort();
  
  let venues = [...new Set(rows.map(s => s.san))];
  venues.sort((a,b) => {
    const idxA = VENUE_NATURAL_ORDER.indexOf(a);
    const idxB = VENUE_NATURAL_ORDER.indexOf(b);
    return (idxA !== -1 ? idxA : 999) - (idxB !== -1 ? idxB : 999);
  });

  const cw = Math.max(150, Math.floor(1000 / venues.length));
  
  let tbl = `<table class="border-collapse w-full text-xs" style="min-width:${venues.length * cw + 110}px">
    <thead>
      <tr class="bg-slate-900 text-white uppercase tracking-wider text-[11px]">
        <th class="px-3 py-3 text-left w-24 sticky left-0 bg-slate-900 z-30 border-r border-slate-700">Khung giờ</th>
        ${venues.map(v => {
          const pfx = v.split('.')[0];
          let headerBadge = '';
          if (pfx === 'NV') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-purple-500/30 text-purple-200 text-[10px] mr-1 font-bold">NV</span>';
          else if (pfx === 'PK') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-orange-500/30 text-orange-200 text-[10px] mr-1 font-bold">PK</span>';
          else if (pfx === 'BĐ') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-green-500/30 text-green-200 text-[10px] mr-1 font-bold">BĐ</span>';
          else if (pfx === 'CL') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-red-500/30 text-red-200 text-[10px] mr-1 font-bold">CL</span>';
          else if (pfx === 'BB') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-blue-500/30 text-blue-200 text-[10px] mr-1 font-bold">BB</span>';
          else if (pfx === 'KC') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-amber-500/30 text-amber-200 text-[10px] mr-1 font-bold">KC</span>';
          else if (pfx === 'BƠI') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-sky-500/30 text-sky-200 text-[10px] mr-1 font-bold">BƠI</span>';
          
          return `<th class="px-2 py-3 text-center font-bold border-r border-slate-700 last:border-0" style="min-width:${cw}px">
            <div class="flex items-center justify-center gap-1">${headerBadge}<span>${escHtml(v)}</span></div>
          </th>`;
        }).join('')}
      </tr>
    </thead>
    <tbody>`;

  timeSlots.forEach((t, i) => {
    const rowData = rows.filter(s => s.batdau === t);
    const end = rowData[0]?.ketthuc || '';
    const luot = rowData[0]?.luot ? `<span class="text-[10px] text-indigo-600 font-bold block">${rowData[0].luot}</span>` : '';
    
    tbl += `<tr class="${i % 2 === 0 ? 'bg-white' : 'bg-slate-50/70'} hover:bg-indigo-50/40 transition">
      <td class="px-3 py-2 font-bold text-slate-700 sticky left-0 ${i % 2 === 0 ? 'bg-white' : 'bg-slate-50'} z-10 border-r border-slate-200 whitespace-nowrap shadow-[1px_0_3px_rgba(0,0,0,0.04)]">
        <span class="text-indigo-700 text-sm">${t}</span>
        <span class="text-slate-400 font-normal block text-[11px]">${end ? '– ' + end : ''}</span>
        ${luot}
      </td>`;
      
    venues.forEach(v => {
      const cells = rowData.filter(s => s.san === v);
      if (cells.length > 0) {
        tbl += `<td class="px-1.5 py-1.5 align-top border-r border-slate-100 last:border-0 space-y-1">`;
        cells.forEach(cell => {
          const col = MON_COLORS[cell.mon] || '#64748b';
          const disp = q ? hl(cell.noiDung, q) : escHtml(cell.noiDung);
          const cd = JSON.stringify(cell).replace(/'/g,"&#39;");
          tbl += `
            <div class="schedule-cell text-white font-medium" style="background:${col}" onclick='showScheduleDetail(${cd})'>
              <span class="font-extrabold block opacity-90 text-[10px] uppercase tracking-wide">${escHtml(cell.mon)}</span>
              <span class="font-medium">${disp}</span>
            </div>`;
        });
        tbl += `</td>`;
      } else {
        tbl += `<td class="px-1.5 py-1.5 border-r border-slate-100 last:border-0"></td>`;
      }
    });
    
    tbl += '</tr>';
  });
  
  tbl += '</tbody></table>';
  document.getElementById('schedule-grid').innerHTML = tbl;
}

function showScheduleDetail(s) {
  const col = MON_COLORS[s.mon] || '#64748b';
  let extraDetail = '';
  if (s.mon === 'Bơi' || (s.san && s.san.includes('BƠI'))) {
    extraDetail = `<div class="mt-3 pt-3 border-t border-slate-200">
      <div class="text-[11px] font-bold text-slate-700 uppercase tracking-wider mb-2">🏊 Chi tiết các lượt thi & 6 làn bơi:</div>
      ${renderSquadForMatch(s.noiDung, s.mon)}
    </div>`;
  }
  showModal(s.mon, `${s.san} · ${s.batdau} - ${s.ketthuc}`,
    `<div class="bg-slate-50 rounded-xl p-4 space-y-3 text-xs">
      <div class="flex gap-3"><span class="text-slate-400 w-24 flex-shrink-0 font-medium">📅 Ngày</span><span class="font-bold text-slate-800">${DAY_LABELS[s.ngay]}</span></div>
      <div class="flex gap-3"><span class="text-slate-400 w-24 flex-shrink-0 font-medium">⏰ Khung giờ</span><span class="font-bold text-slate-800">${s.batdau} – ${s.ketthuc} ${s.luot ? '(' + s.luot + ')' : ''}</span></div>
      <div class="flex gap-3"><span class="text-slate-400 w-24 flex-shrink-0 font-medium">🏟️ Sân / Bàn</span><span class="font-bold text-indigo-700">${escHtml(s.san)}</span></div>
      <div class="flex gap-3"><span class="text-slate-400 w-24 flex-shrink-0 font-medium">📍 Khu vực</span><span class="font-semibold text-slate-700">${escHtml(s.khuVuc || '')}</span></div>
      <div class="flex gap-3"><span class="text-slate-400 w-24 flex-shrink-0 font-medium">📋 Nội dung</span><span class="font-bold text-slate-900 bg-white p-2.5 rounded border border-slate-200 flex-1 leading-relaxed">${escHtml(s.noiDung)}</span></div>
      ${extraDetail}
    </div>`, col);
}'''

new_render_schedule = '''function renderSchedule() {
  // 1. Compute Live Tournament State before rendering
  updateAllTournamentsLiveState();

  const monF = document.getElementById('filter-mon-sch').value;
  const sanF = document.getElementById('filter-san-sch').value;
  const q = (document.getElementById('search-team').value || '').trim().toLowerCase();
  
  let rows = DATA.schedule.filter(s => s.ngay === currentDay);
  if (monF) rows = rows.filter(s => s.mon === monF);
  if (sanF) rows = rows.filter(s => s.san === sanF);
  if (q) rows = rows.filter(s => {
    const live = findMatchForScheduleCell(s);
    const liveTeams = live && live.hasLiveTeams ? `${live.team1.name} ${live.team2.name}`.toLowerCase() : '';
    return s.noiDung.toLowerCase().includes(q) || s.san.toLowerCase().includes(q) || s.mon.toLowerCase().includes(q) || liveTeams.includes(q);
  });
  
  document.getElementById('sch-count').textContent = rows.length + ' trận/ô lịch';
  
  if (!rows.length) {
    document.getElementById('schedule-grid').innerHTML = `
      <div class="p-12 text-center text-slate-400">
        <div class="text-4xl mb-2">📋</div>
        <p class="font-bold text-sm text-slate-600">Không có lịch thi đấu phù hợp với bộ lọc</p>
        <p class="text-xs text-slate-400 mt-1">Hãy thử chọn ngày khác hoặc bỏ bớt tiêu chí lọc</p>
      </div>`;
    return;
  }

  const timeSlots = [...new Set(rows.map(s => s.batdau))].sort();
  
  let venues = [...new Set(rows.map(s => s.san))];
  venues.sort((a,b) => {
    const idxA = VENUE_NATURAL_ORDER.indexOf(a);
    const idxB = VENUE_NATURAL_ORDER.indexOf(b);
    return (idxA !== -1 ? idxA : 999) - (idxB !== -1 ? idxB : 999);
  });

  const cw = Math.max(160, Math.floor(1000 / venues.length));
  
  let tbl = `<table class="border-collapse w-full text-xs" style="min-width:${venues.length * cw + 110}px">
    <thead>
      <tr class="bg-slate-900 text-white uppercase tracking-wider text-[11px]">
        <th class="px-3 py-3 text-left w-24 sticky left-0 bg-slate-900 z-30 border-r border-slate-700">Khung giờ</th>
        ${venues.map(v => {
          const pfx = v.split('.')[0];
          let headerBadge = '';
          if (pfx === 'NV') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-purple-500/30 text-purple-200 text-[10px] mr-1 font-bold">NV</span>';
          else if (pfx === 'PK') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-orange-500/30 text-orange-200 text-[10px] mr-1 font-bold">PK</span>';
          else if (pfx === 'BĐ') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-green-500/30 text-green-200 text-[10px] mr-1 font-bold">BĐ</span>';
          else if (pfx === 'CL') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-red-500/30 text-red-200 text-[10px] mr-1 font-bold">CL</span>';
          else if (pfx === 'BB') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-blue-500/30 text-blue-200 text-[10px] mr-1 font-bold">BB</span>';
          else if (pfx === 'KC') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-amber-500/30 text-amber-200 text-[10px] mr-1 font-bold">KC</span>';
          else if (pfx === 'BƠI') headerBadge = '<span class="px-1.5 py-0.5 rounded bg-sky-500/30 text-sky-200 text-[10px] mr-1 font-bold">BƠI</span>';
          
          return `<th class="px-2 py-3 text-center font-bold border-r border-slate-700 last:border-0" style="min-width:${cw}px">
            <div class="flex items-center justify-center gap-1">${headerBadge}<span>${escHtml(v)}</span></div>
          </th>`;
        }).join('')}
      </tr>
    </thead>
    <tbody>`;

  timeSlots.forEach((t, i) => {
    const rowData = rows.filter(s => s.batdau === t);
    const end = rowData[0]?.ketthuc || '';
    const luot = rowData[0]?.luot ? `<span class="text-[10px] text-indigo-600 font-bold block">${rowData[0].luot}</span>` : '';
    
    tbl += `<tr class="${i % 2 === 0 ? 'bg-white' : 'bg-slate-50/70'} hover:bg-indigo-50/40 transition">
      <td class="px-3 py-2 font-bold text-slate-700 sticky left-0 ${i % 2 === 0 ? 'bg-white' : 'bg-slate-50'} z-10 border-r border-slate-200 whitespace-nowrap shadow-[1px_0_3px_rgba(0,0,0,0.04)]">
        <span class="text-indigo-700 text-sm font-black">${t}</span>
        <span class="text-slate-400 font-normal block text-[11px]">${end ? '– ' + end : ''}</span>
        ${luot}
      </td>`;
      
    venues.forEach(v => {
      const cells = rowData.filter(s => s.san === v);
      if (cells.length > 0) {
        tbl += `<td class="px-1.5 py-1.5 align-top border-r border-slate-100 last:border-0 space-y-1">`;
        cells.forEach(cell => {
          const col = MON_COLORS[cell.mon] || '#64748b';
          const cd = JSON.stringify(cell).replace(/'/g,"&#39;");
          const liveInfo = findMatchForScheduleCell(cell);
          
          if (liveInfo && liveInfo.hasLiveTeams) {
            // LIVE TEAMS DETERMINED FROM BRACKET PROGRESSION
            const mCode = liveInfo.matchCode || liveInfo.match.id;
            const t1 = liveInfo.team1.name;
            const t2 = liveInfo.team2.name;
            const scoreBadge = liveInfo.hasScore
              ? `<div class="mt-1 pt-0.5 border-t border-white/20 flex items-center justify-between text-[10px]">
                   <span class="text-amber-200 font-bold">Tỉ số:</span>
                   <span class="px-1.5 py-0.2 rounded bg-black/40 font-mono font-black text-amber-300 text-xs">${liveInfo.scores.s1} - ${liveInfo.scores.s2}</span>
                 </div>`
              : '';
            
            tbl += `
              <div class="schedule-cell text-white font-medium relative border-l-4 border-amber-300 shadow-sm cursor-pointer hover:brightness-110 transition" 
                   style="background:${col}" onclick='showScheduleDetail(${cd})' title="Đã tự động cập nhật tên đội từ sơ đồ thi đấu!">
                <div class="flex items-center justify-between gap-1 mb-0.5">
                  <span class="font-extrabold block opacity-90 text-[10px] uppercase tracking-wide truncate">${escHtml(cell.mon)}</span>
                  <span class="px-1 py-0.2 rounded bg-amber-400 text-amber-950 font-black text-[9px] uppercase tracking-tight shadow-xs flex-shrink-0">⚡ ${escHtml(mCode)}</span>
                </div>
                <div class="text-[11px] leading-snug font-bold text-amber-100">
                  <span class="text-white">${escHtml(t1)}</span>
                  <span class="text-amber-300 font-black mx-0.5">vs</span>
                  <span class="text-white">${escHtml(t2)}</span>
                </div>
                ${scoreBadge}
              </div>`;
          } else if (liveInfo && liveInfo.hasScore) {
            // MATCH WITH RECORDED SCORE
            const disp = q ? hl(cell.noiDung, q) : escHtml(cell.noiDung);
            tbl += `
              <div class="schedule-cell text-white font-medium relative shadow-sm cursor-pointer hover:brightness-110 transition" 
                   style="background:${col}" onclick='showScheduleDetail(${cd})'>
                <div class="flex items-center justify-between gap-1 mb-0.5">
                  <span class="font-extrabold block opacity-90 text-[10px] uppercase tracking-wide truncate">${escHtml(cell.mon)}</span>
                  <span class="px-1.5 py-0.2 rounded bg-black/40 font-mono font-black text-amber-300 text-[10px] flex-shrink-0">${liveInfo.scores.s1} - ${liveInfo.scores.s2}</span>
                </div>
                <span class="font-medium">${disp}</span>
              </div>`;
          } else {
            // ORIGINAL SCHEDULE CONTENT
            const disp = q ? hl(cell.noiDung, q) : escHtml(cell.noiDung);
            tbl += `
              <div class="schedule-cell text-white font-medium cursor-pointer hover:brightness-110 transition" 
                   style="background:${col}" onclick='showScheduleDetail(${cd})'>
                <span class="font-extrabold block opacity-90 text-[10px] uppercase tracking-wide truncate">${escHtml(cell.mon)}</span>
                <span class="font-medium">${disp}</span>
              </div>`;
          }
        });
        tbl += `</td>`;
      } else {
        tbl += `<td class="px-1.5 py-1.5 border-r border-slate-100 last:border-0"></td>`;
      }
    });
    
    tbl += '</tr>';
  });
  
  tbl += '</tbody></table>';
  document.getElementById('schedule-grid').innerHTML = tbl;
}

function showScheduleDetail(s) {
  const col = MON_COLORS[s.mon] || '#64748b';
  const liveInfo = findMatchForScheduleCell(s);

  let liveCardHtml = '';
  let squadsHtml = '';

  if (liveInfo) {
    const t1Athletes = findAthletesForTeam(liveInfo.team1, s.mon);
    const t2Athletes = findAthletesForTeam(liveInfo.team2, s.mon);
    
    liveCardHtml = `
      <div class="bg-gradient-to-br from-amber-500/10 via-amber-100/40 to-indigo-50 rounded-xl p-3.5 border border-amber-300 shadow-xs space-y-2.5">
        <div class="flex items-center justify-between border-b border-amber-200/80 pb-2">
          <div class="flex items-center gap-1.5">
            <span class="px-2 py-0.5 rounded bg-amber-500 text-white font-black text-[11px] shadow-2xs">${escHtml(liveInfo.matchCode || liveInfo.match.id)}</span>
            <strong class="text-slate-900 font-extrabold text-xs">${escHtml(liveInfo.tour.name)}</strong>
          </div>
          <span class="text-[10px] font-bold text-amber-900 bg-amber-200/80 px-2 py-0.5 rounded-full flex items-center gap-1">
            <span>⚡</span> Đồng bộ Tab Kết quả
          </span>
        </div>

        ${liveInfo.hasLiveTeams ? `
          <!-- CẶP ĐẤU ĐÃ XÁC ĐỊNH -->
          <div class="grid grid-cols-2 gap-2 bg-white p-2.5 rounded-lg border border-slate-200">
            <div class="text-center p-2 rounded-lg ${liveInfo.isDecided && liveInfo.winner === liveInfo.team1 ? 'bg-emerald-50 border border-emerald-300' : 'bg-slate-50'}">
              <span class="text-[10px] font-bold text-slate-400 block">${liveInfo.team1.code ? escHtml(liveInfo.team1.code) : 'Đội 1'}</span>
              <strong class="font-black text-slate-900 text-xs block mt-0.5 truncate">${escHtml(liveInfo.team1.name)}</strong>
              ${liveInfo.team1.sub ? `<span class="text-[10px] text-slate-500 block truncate">${escHtml(liveInfo.team1.sub)}</span>` : ''}
              ${liveInfo.isDecided && liveInfo.winner === liveInfo.team1 ? '<span class="inline-block mt-1 px-1.5 py-0.5 bg-emerald-600 text-white text-[9px] font-black rounded">🏆 Thắng trận</span>' : ''}
            </div>

            <div class="text-center p-2 rounded-lg ${liveInfo.isDecided && liveInfo.winner === liveInfo.team2 ? 'bg-emerald-50 border border-emerald-300' : 'bg-slate-50'}">
              <span class="text-[10px] font-bold text-slate-400 block">${liveInfo.team2.code ? escHtml(liveInfo.team2.code) : 'Đội 2'}</span>
              <strong class="font-black text-slate-900 text-xs block mt-0.5 truncate">${escHtml(liveInfo.team2.name)}</strong>
              ${liveInfo.team2.sub ? `<span class="text-[10px] text-slate-500 block truncate">${escHtml(liveInfo.team2.sub)}</span>` : ''}
              ${liveInfo.isDecided && liveInfo.winner === liveInfo.team2 ? '<span class="inline-block mt-1 px-1.5 py-0.5 bg-emerald-600 text-white text-[9px] font-black rounded">🏆 Thắng trận</span>' : ''}
            </div>
          </div>

          <!-- TỈ SỐ HIỆN TẠI -->
          <div class="flex items-center justify-between px-3 py-2 bg-white rounded-lg border border-slate-200 text-xs">
            <span class="font-bold text-slate-600">Tỉ số trận đấu:</span>
            ${liveInfo.hasScore 
              ? `<span class="font-mono font-black text-sm text-indigo-700 bg-indigo-50 px-3 py-0.5 rounded-lg border border-indigo-200">${liveInfo.scores.s1} - ${liveInfo.scores.s2}</span>`
              : '<span class="text-slate-400 italic font-semibold">Chưa có kết quả (chưa đấu)</span>'}
          </div>
        ` : `
          <!-- CHƯA XÁC ĐỊNH ĐỘI -->
          <div class="bg-amber-100/70 p-2.5 rounded-lg border border-amber-200/90 text-amber-950 text-xs space-y-1">
            <div class="flex items-center gap-1.5 font-bold">
              <span>⏳</span>
              <span>Chưa xác định 2 đội thi đấu</span>
            </div>
            <p class="text-[11px] text-amber-900 leading-relaxed">
              Trận đấu này sẽ <strong>tự động cập nhật tên 2 đội</strong> ngay khi có kết quả từ các trận trước (Vòng bảng / Tứ kết) tại Tab Kết quả.
            </p>
          </div>
        `}

        <!-- NÚT CHUYỂN NHANH SANG TAB KẾT QUẢ -->
        <button onclick="switchToTournamentTab('${liveInfo.tour.id}', '${liveInfo.match.id}')"
          class="w-full py-2 px-3 bg-gradient-to-r from-amber-500 to-indigo-600 hover:from-amber-600 hover:to-indigo-700 text-white font-bold rounded-xl shadow-xs text-xs flex items-center justify-center gap-2 transition cursor-pointer">
          <span>🏆</span>
          <span>Xem sơ đồ & Nhập kết quả môn ${escHtml(liveInfo.tour.name)}</span>
          <span class="text-amber-200 font-bold">➔</span>
        </button>
      </div>`;

    if (t1Athletes.length > 0 || t2Athletes.length > 0) {
      squadsHtml = `
        <div class="mt-3 pt-3 border-t border-slate-200 space-y-2">
          <div class="text-[11px] font-bold text-slate-700 uppercase tracking-wider">👥 Danh sách VĐV của 2 đội:</div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
            <!-- ĐỘI 1 -->
            <div class="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
              <strong class="text-indigo-900 block mb-1 text-xs">🔹 ${escHtml(liveInfo.team1.name)} (${t1Athletes.length} VĐV):</strong>
              <div class="flex flex-wrap gap-1">
                ${t1Athletes.map(a => `<span class="px-2 py-0.5 rounded bg-slate-100 text-slate-800 text-[11px] border border-slate-200">${escHtml(a.hoVaTen)}</span>`).join('')}
              </div>
            </div>
            <!-- ĐỘI 2 -->
            <div class="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
              <strong class="text-indigo-900 block mb-1 text-xs">🔹 ${escHtml(liveInfo.team2.name)} (${t2Athletes.length} VĐV):</strong>
              <div class="flex flex-wrap gap-1">
                ${t2Athletes.map(a => `<span class="px-2 py-0.5 rounded bg-slate-100 text-slate-800 text-[11px] border border-slate-200">${escHtml(a.hoVaTen)}</span>`).join('')}
              </div>
            </div>
          </div>
        </div>`;
    }
  }

  let extraDetail = '';
  if (s.mon === 'Bơi' || (s.san && s.san.includes('BƠI'))) {
    extraDetail = `<div class="mt-3 pt-3 border-t border-slate-200">
      <div class="text-[11px] font-bold text-slate-700 uppercase tracking-wider mb-2">🏊 Chi tiết các lượt thi & 6 làn bơi:</div>
      ${renderSquadForMatch(s.noiDung, s.mon)}
      <button onclick="switchToTournamentTab('swimming', '')"
        class="w-full mt-2.5 py-2 px-3 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-600 hover:to-indigo-700 text-white font-bold rounded-xl shadow-xs text-xs flex items-center justify-center gap-2 transition cursor-pointer">
        <span>🏊</span>
        <span>Xem sơ đồ & Nhập thời gian thi đấu Môn Bơi</span>
        <span class="text-sky-200 font-bold">➔</span>
      </button>
    </div>`;
  } else if (!squadsHtml) {
    extraDetail = `<div class="mt-3 pt-3 border-t border-slate-200">
      <div class="text-[11px] font-bold text-slate-700 uppercase tracking-wider mb-2">👥 Đội hình / VĐV tham gia:</div>
      ${renderSquadForMatch(s.noiDung, s.mon)}
    </div>`;
  }

  showModal(s.mon, `${s.san} · ${s.batdau} - ${s.ketthuc}`,
    `<div class="bg-slate-50 rounded-xl p-4 space-y-3 text-xs">
      ${liveCardHtml}
      <div class="flex gap-3"><span class="text-slate-400 w-24 flex-shrink-0 font-medium">📅 Ngày</span><span class="font-bold text-slate-800">${DAY_LABELS[s.ngay]}</span></div>
      <div class="flex gap-3"><span class="text-slate-400 w-24 flex-shrink-0 font-medium">⏰ Khung giờ</span><span class="font-bold text-slate-800">${s.batdau} – ${s.ketthuc} ${s.luot ? '(' + s.luot + ')' : ''}</span></div>
      <div class="flex gap-3"><span class="text-slate-400 w-24 flex-shrink-0 font-medium">🏟️ Sân / Bàn</span><span class="font-bold text-indigo-700">${escHtml(s.san)}</span></div>
      <div class="flex gap-3"><span class="text-slate-400 w-24 flex-shrink-0 font-medium">📍 Khu vực</span><span class="font-semibold text-slate-700">${escHtml(s.khuVuc || '')}</span></div>
      <div class="flex gap-3"><span class="text-slate-400 w-24 flex-shrink-0 font-medium">📋 Nội dung</span><span class="font-bold text-slate-900 bg-white p-2.5 rounded border border-slate-200 flex-1 leading-relaxed">${escHtml(s.noiDung)}</span></div>
      ${squadsHtml}
      ${extraDetail}
    </div>`, col);
}'''

if old_render_schedule in content:
    content = content.replace(old_render_schedule, new_render_schedule)
    print("Updated renderSchedule and showScheduleDetail with Live Synchronization!")
else:
    print("Error: old_render_schedule not found in template!")
    sys.exit(1)

# ================================================================
# SECTION 4: UPDATE TAB 5 JAVASCRIPT IMPLEMENTATION
# ================================================================
new_tab5_js = '''// ================================================================
// TAB 5: RESULTS & TOURNAMENT BRACKET ENGINE (SƠ ĐỒ CÂY TỪ TRÁI SANG PHẢI & TÍNH ĐIỂM TỰ ĐỘNG)
// ================================================================
let currentTourId = 'bd_m';
let currentTourSportFilter = 'all';
let currentSwimSubEvent = 'swim_m_td40';

function initResults() {
  updateAllTournamentsLiveState();
  populateTournamentSelect();
  renderTournamentView();
}

function renderResults() {
  updateAllTournamentsLiveState();
  renderTournamentView();
}

function populateTournamentSelect() {
  const sel = document.getElementById('active-tournament-select');
  if (!sel) return;
  sel.innerHTML = '';
  
  const tournaments = DATA.tournaments || [];
  let filtered = tournaments;
  if (currentTourSportFilter !== 'all') {
    filtered = tournaments.filter(t => t.sport === currentTourSportFilter);
  }
  
  if (!filtered.some(t => t.id === currentTourId)) {
    if (filtered.length > 0) currentTourId = filtered[0].id;
  }
  
  // Group options by sport
  const sports = [...new Set(filtered.map(t => t.sport))];
  sports.forEach(sp => {
    const group = document.createElement('optgroup');
    group.label = 'Môn ' + sp;
    filtered.filter(t => t.sport === sp).forEach(t => {
      const opt = document.createElement('option');
      opt.value = t.id;
      opt.textContent = `${t.name} (${t.code})`;
      if (t.id === currentTourId) opt.selected = true;
      group.appendChild(opt);
    });
    sel.appendChild(group);
  });
}

function filterTourBySport(sport, btn) {
  currentTourSportFilter = sport;
  document.querySelectorAll('.tour-pill').forEach(p => {
    p.className = 'tour-pill px-3 py-1.5 rounded-lg text-xs font-bold transition bg-slate-100 text-slate-700 hover:bg-slate-200';
  });
  if (btn) btn.className = 'tour-pill px-3 py-1.5 rounded-lg text-xs font-bold transition bg-slate-800 text-white shadow-sm';
  populateTournamentSelect();
  renderTournamentView();
}

function onTournamentSelectChange(tourId) {
  currentTourId = tourId;
  renderTournamentView();
}

function onScoreChange(tourId, matchId, teamNum, val) {
  if (!tourScores[tourId]) tourScores[tourId] = {};
  if (!tourScores[tourId][matchId]) tourScores[tourId][matchId] = {};
  
  const cleanVal = val.trim();
  const num = cleanVal !== '' && !isNaN(Number(cleanVal)) ? Number(cleanVal) : null;
  
  if (teamNum === 1) tourScores[tourId][matchId].s1 = num;
  if (teamNum === 2) tourScores[tourId][matchId].s2 = num;
  
  saveTourScores();
  updateAllTournamentsLiveState();
  renderTournamentView();
  
  // Re-render schedule if tab-schedule is currently visible or in DOM
  renderSchedule();
}

function onSwimTimeChange(tourId, subEventId, heatId, laneNum, val) {
  if (!tourScores[tourId]) tourScores[tourId] = {};
  if (!tourScores[tourId][subEventId]) tourScores[tourId][subEventId] = {};
  if (!tourScores[tourId][subEventId][heatId]) tourScores[tourId][subEventId][heatId] = {};
  
  tourScores[tourId][subEventId][heatId][laneNum] = val.trim();
  saveTourScores();
  updateAllTournamentsLiveState();
  renderTournamentView();
  renderSchedule();
}

function parseSwimTime(str) {
  if (!str) return 999999;
  const s = String(str).trim();
  if (s.includes(':')) {
    const parts = s.split(':');
    const mins = parseFloat(parts[0]) || 0;
    const secs = parseFloat(parts[1]) || 0;
    return mins * 60 + secs;
  }
  const secs = parseFloat(s);
  return isNaN(secs) ? 999999 : secs;
}

// Universal match card renderer
function renderMatchCard(tourId, match, options = {}) {
  const scores = (tourScores[tourId] && tourScores[tourId][match.id]) || {};
  const s1Val = scores.s1 !== null && scores.s1 !== undefined ? scores.s1 : '';
  const s2Val = scores.s2 !== null && scores.s2 !== undefined ? scores.s2 : '';
  
  const hasResult = s1Val !== '' && s2Val !== '';
  const win1 = hasResult && Number(s1Val) > Number(s2Val);
  const win2 = hasResult && Number(s2Val) > Number(s1Val);
  
  const t1 = match.team1 || { name: match.source1 || 'Chờ xác định', isPlaceholder: true };
  const t2 = match.team2 || { name: match.source2 || 'Chờ xác định', isPlaceholder: true };
  const isMatchReady = !t1.isPlaceholder && !t2.isPlaceholder;
  
  const isFinalCard = options.isFinal || match.isFinal;
  const isThirdPlaceCard = options.isThirdPlace || match.isThirdPlace;
  
  let headerBadge = `<span class="font-extrabold text-[11px] text-indigo-700">${escHtml(match.name || match.id)}</span>`;
  if (isFinalCard) {
    headerBadge = `<span class="font-black text-[11px] text-amber-700 uppercase flex items-center gap-1">🏆 ${escHtml(match.name || 'CHUNG KẾT')}</span>`;
  } else if (isThirdPlaceCard) {
    headerBadge = `<span class="font-bold text-[11px] text-amber-800 uppercase flex items-center gap-1">🥉 ${escHtml(match.name || 'TRANH 3-4')}</span>`;
  }

  const borderClass = isFinalCard ? 'border-amber-400 bg-amber-50/20' : isThirdPlaceCard ? 'border-amber-300 bg-slate-50/60' : 'border-slate-200 bg-white';

  return `
    <div class="bracket-card ${borderClass} rounded-xl p-3 shadow-xs space-y-2">
      <!-- MATCH HEADER -->
      <div class="flex items-center justify-between text-[11px] border-b border-slate-100 pb-1.5">
        ${headerBadge}
        <span class="text-slate-400 font-semibold text-[10px]">${escHtml(match.time || '')} · ${escHtml(match.venue || '')}</span>
      </div>

      <!-- TEAMS & SCORES -->
      <div class="space-y-1.5">
        <!-- TEAM 1 -->
        <div class="bracket-team-row ${win1 ? 'winner' : win2 ? 'loser' : ''}">
          <div class="flex items-center gap-1.5 min-w-0 flex-1">
            <span class="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold ${win1 ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-700'}">${escHtml(t1.code || '1')}</span>
            <div class="min-w-0 flex-1">
              <p class="font-bold text-xs truncate leading-tight ${t1.isPlaceholder ? 'text-slate-400 italic font-normal' : 'text-slate-900'}">${escHtml(t1.name)}</p>
              ${t1.sub ? `<p class="text-[10px] text-slate-400 truncate">${escHtml(t1.sub)}</p>` : ''}
            </div>
          </div>
          <input type="number" min="0" value="${s1Val}" placeholder="-" 
            ${!isMatchReady ? 'disabled' : ''}
            class="bracket-score-input ${!isMatchReady ? 'opacity-40 cursor-not-allowed bg-slate-100' : ''}"
            oninput="onScoreChange('${tourId}', '${match.id}', 1, this.value)">
        </div>

        <!-- TEAM 2 -->
        <div class="bracket-team-row ${win2 ? 'winner' : win1 ? 'loser' : ''}">
          <div class="flex items-center gap-1.5 min-w-0 flex-1">
            <span class="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold ${win2 ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-700'}">${escHtml(t2.code || '2')}</span>
            <div class="min-w-0 flex-1">
              <p class="font-bold text-xs truncate leading-tight ${t2.isPlaceholder ? 'text-slate-400 italic font-normal' : 'text-slate-900'}">${escHtml(t2.name)}</p>
              ${t2.sub ? `<p class="text-[10px] text-slate-400 truncate">${escHtml(t2.sub)}</p>` : ''}
            </div>
          </div>
          <input type="number" min="0" value="${s2Val}" placeholder="-" 
            ${!isMatchReady ? 'disabled' : ''}
            class="bracket-score-input ${!isMatchReady ? 'opacity-40 cursor-not-allowed bg-slate-100' : ''}"
            oninput="onScoreChange('${tourId}', '${match.id}', 2, this.value)">
        </div>
      </div>
    </div>`;
}

// Podium component renderer
function renderPodiumBox(gold, silver, bronze, fourth) {
  const isGoldValid = gold && !gold.isPlaceholder;
  const isSilverValid = silver && !silver.isPlaceholder;
  const isBronzeValid = bronze && !bronze.isPlaceholder;
  const isFourthValid = fourth && !fourth.isPlaceholder;

  return `
    <div class="podium-box">
      <div class="text-center pb-3 border-b border-amber-200/80 mb-3">
        <span class="text-3xl block mb-1">🏆</span>
        <h4 class="font-black text-sm uppercase tracking-wider text-amber-950">BỤC VINH QUANG</h4>
        <p class="text-[11px] text-amber-800 font-medium">Thứ hạng chung cuộc</p>
      </div>

      <div class="space-y-2.5 text-xs">
        <!-- GOLD 1ST -->
        <div class="bg-white/90 p-2.5 rounded-xl border border-amber-300 shadow-2xs flex items-center gap-2.5">
          <span class="text-2xl flex-shrink-0">🥇</span>
          <div class="min-w-0 flex-1">
            <span class="text-[10px] font-black uppercase text-amber-600 block">VÔ ĐỊCH (HCV)</span>
            ${isGoldValid ? `
              <strong class="text-slate-900 text-sm truncate block font-black">${escHtml(gold.name)}</strong>
              ${gold.sub ? `<span class="text-[10px] text-slate-500 block truncate">${escHtml(gold.sub)}</span>` : ''}
            ` : '<span class="text-slate-400 italic font-normal text-xs">Chờ chung kết</span>'}
          </div>
        </div>

        <!-- SILVER 2ND -->
        <div class="bg-white/70 p-2 rounded-xl border border-slate-200 flex items-center gap-2.5">
          <span class="text-xl flex-shrink-0">🥈</span>
          <div class="min-w-0 flex-1">
            <span class="text-[10px] font-black uppercase text-slate-500 block">Á QUÂN (HCB)</span>
            ${isSilverValid ? `
              <strong class="text-slate-800 text-xs truncate block font-bold">${escHtml(silver.name)}</strong>
            ` : '<span class="text-slate-400 italic font-normal text-xs">Chờ chung kết</span>'}
          </div>
        </div>

        <!-- BRONZE 3RD -->
        <div class="bg-white/70 p-2 rounded-xl border border-amber-200/60 flex items-center gap-2.5">
          <span class="text-xl flex-shrink-0">🥉</span>
          <div class="min-w-0 flex-1">
            <span class="text-[10px] font-black uppercase text-amber-700 block">HẠNG BA (HCĐ)</span>
            ${isBronzeValid ? `
              <strong class="text-slate-800 text-xs truncate block font-bold">${escHtml(bronze.name)}</strong>
            ` : '<span class="text-slate-400 italic font-normal text-xs">Chờ tranh 3-4</span>'}
          </div>
        </div>

        <!-- 4TH -->
        ${fourth ? `
        <div class="bg-white/50 p-1.5 px-2.5 rounded-lg border border-slate-200/60 flex items-center gap-2 text-[11px]">
          <span class="font-bold text-slate-400">4️⃣</span>
          <span class="text-slate-500 truncate flex-1 font-semibold">Hạng Tư: <strong>${escHtml(fourth.name)}</strong></span>
        </div>` : ''}
      </div>
    </div>`;
}

// Standings Table Renderer
function renderStandingsTable(standings, isFootball = false, qualifyTop = 2) {
  const hasPlayedAny = standings.some(s => s.played > 0);
  return `
    <div class="overflow-x-auto bg-white rounded-xl border border-slate-200 shadow-2xs">
      <table class="w-full text-xs text-left">
        <thead class="bg-slate-900 text-white text-[10px] uppercase font-bold">
          <tr>
            <th class="px-2.5 py-2 text-center w-8">Hạng</th>
            <th class="px-2.5 py-2">Đội thi</th>
            <th class="px-2 py-2 text-center" title="Số trận">Trận</th>
            <th class="px-2 py-2 text-center" title="Thắng">T</th>
            ${isFootball ? '<th class="px-2 py-2 text-center" title="Hòa">H</th>' : ''}
            <th class="px-2 py-2 text-center" title="Bại">B</th>
            <th class="px-2 py-2 text-center" title="Bàn thắng / thua">${isFootball ? 'BT-BB' : 'Séc'}</th>
            <th class="px-2 py-2 text-center font-black text-indigo-300">Điểm</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          ${standings.map((st, idx) => {
            const isQual = hasPlayedAny && idx < qualifyTop && st.played > 0;
            const rankBadge = isQual 
              ? `<span class="w-5 h-5 rounded-full bg-emerald-600 text-white font-black inline-flex items-center justify-center text-[11px] shadow-2xs">${idx + 1}</span>`
              : `<span class="w-5 h-5 rounded-full bg-slate-200 text-slate-600 font-bold inline-flex items-center justify-center text-[11px]">${idx + 1}</span>`;
            
            return `
              <tr class="${isQual ? 'bg-emerald-50/30' : ''} hover:bg-slate-50 transition">
                <td class="px-2.5 py-2 text-center font-bold">${rankBadge}</td>
                <td class="px-2.5 py-2 font-bold text-slate-800">
                  <div class="flex items-center gap-1.5">
                    <span>${escHtml(st.name)}</span>
                    ${isQual ? '<span class="text-[9px] font-black px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 uppercase tracking-tight">Vào vòng trong</span>' : ''}
                  </div>
                </td>
                <td class="px-2 py-2 text-center text-slate-500">${st.played}</td>
                <td class="px-2 py-2 text-center text-emerald-700 font-bold">${st.won}</td>
                ${isFootball ? `<td class="px-2 py-2 text-center text-slate-500">${st.drawn}</td>` : ''}
                <td class="px-2 py-2 text-center text-rose-600 font-bold">${st.lost}</td>
                <td class="px-2 py-2 text-center font-mono text-slate-600">${st.gf}-${st.ga}</td>
                <td class="px-2 py-2 text-center font-black text-indigo-700 text-sm">${st.points}</td>
              </tr>`;
          }).join('')}
        </tbody>
      </table>
    </div>`;
}

// FORMAT 1: KNOCKOUT 8
function renderKnockout8(tour) {
  const roundTK = tour.rounds.find(r => r.id === 'tk');
  const roundBK = tour.rounds.find(r => r.id === 'bk');
  const roundFN = tour.rounds.find(r => r.id === 'fn');
  
  const mTK = roundTK.matches;
  const mBK = roundBK.matches;
  const mFN = roundFN.matches;
  
  const mCK = mFN.find(m => m.isFinal || m.id.endsWith('CK'));
  const m34 = mFN.find(m => m.isThirdPlace || m.id.includes('3-4') || m.id.includes('Ba-Tư'));
  
  const ckRes = mCK ? getWinnerAndLoser(mCK, (tourScores[tour.id] && tourScores[tour.id][mCK.id]) || {}) : {};
  const t34Res = m34 ? getWinnerAndLoser(m34, (tourScores[tour.id] && tourScores[tour.id][m34.id]) || {}) : {};
  
  const gold = ckRes.winner;
  const silver = ckRes.loser;
  const bronze = t34Res.winner;
  const fourth = t34Res.loser;

  return `
    <div class="bracket-wrapper bg-slate-50/50 rounded-2xl border border-slate-200">
      <div class="bracket-tree">
        <!-- COLUMN 1: TỨ KẾT (4 TRẬN) -->
        <div class="bracket-col">
          <div class="bracket-round-title">1. TỨ KẾT (4 TRẬN)</div>
          <div class="space-y-4">
            ${mTK.map(m => renderMatchCard(tour.id, m)).join('')}
          </div>
        </div>

        <div class="flex items-center justify-center text-slate-300 font-bold text-2xl select-none">➔</div>

        <!-- COLUMN 2: BÁN KẾT (2 TRẬN) -->
        <div class="bracket-col">
          <div class="bracket-round-title">2. BÁN KẾT (2 TRẬN)</div>
          <div class="space-y-12 my-auto">
            ${mBK.map(m => renderMatchCard(tour.id, m)).join('')}
          </div>
        </div>

        <div class="flex items-center justify-center text-slate-300 font-bold text-2xl select-none">➔</div>

        <!-- COLUMN 3: CHUNG KẾT & TRANH 3-4 (2 TRẬN) -->
        <div class="bracket-col">
          <div class="bracket-round-title">3. CHUNG KẾT & TRANH 3-4</div>
          <div class="space-y-6 my-auto">
            ${mCK ? renderMatchCard(tour.id, mCK, { isFinal: true }) : ''}
            ${m34 ? renderMatchCard(tour.id, m34, { isThirdPlace: true }) : ''}
          </div>
        </div>

        <div class="flex items-center justify-center text-amber-400 font-bold text-2xl select-none">➔</div>

        <!-- COLUMN 4: BỤC VINH QUANG 🏆 -->
        <div class="bracket-col min-w-[280px]">
          <div class="bracket-round-title bg-amber-600">4. KẾT QUẢ VINH QUANG</div>
          <div class="my-auto">
            ${renderPodiumBox(gold, silver, bronze, fourth)}
          </div>
        </div>
      </div>
    </div>`;
}

// FORMAT 2: GROUP 2 CROSS (KÉO CO)
function renderGroup2Cross(tour) {
  const grpA = tour.groups[0];
  const grpB = tour.groups[1];
  
  const stdA = computeGroupStandings(grpA, tour.id, false);
  const stdB = computeGroupStandings(grpB, tour.id, false);
  
  const roundBK = tour.knockout.find(r => r.id === 'bk');
  const roundFN = tour.knockout.find(r => r.id === 'fn');
  
  const mCK = roundFN.matches.find(m => m.isFinal || m.id.endsWith('CK'));
  const m34 = roundFN.matches.find(m => m.isThirdPlace || m.id.includes('3-4'));
  
  const ckRes = mCK ? getWinnerAndLoser(mCK, (tourScores[tour.id] && tourScores[tour.id][mCK.id]) || {}) : {};
  const t34Res = m34 ? getWinnerAndLoser(m34, (tourScores[tour.id] && tourScores[tour.id][m34.id]) || {}) : {};

  return `
    <div class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <!-- BẢNG A -->
        <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs space-y-3">
          <div class="flex items-center justify-between border-b border-slate-100 pb-2">
            <h4 class="font-extrabold text-sm text-slate-900 flex items-center gap-1.5">
              <span class="w-2.5 h-2.5 rounded-full bg-amber-600 inline-block"></span> ${escHtml(grpA.name)}
            </h4>
            <span class="text-[11px] text-slate-500 font-semibold">6 trận đấu vòng tròn</span>
          </div>
          ${renderStandingsTable(stdA, false, 2)}
          <div class="pt-2">
            <h5 class="text-[11px] font-bold uppercase text-slate-500 mb-2">Nhập kết quả các trận Bảng A:</h5>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              ${grpA.matches.map(m => {
                const fullM = { ...m, team1: grpA.teams.find(x => x.id === m.team1), team2: grpA.teams.find(x => x.id === m.team2) };
                return renderMatchCard(tour.id, fullM);
              }).join('')}
            </div>
          </div>
        </div>

        <!-- BẢNG B -->
        <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs space-y-3">
          <div class="flex items-center justify-between border-b border-slate-100 pb-2">
            <h4 class="font-extrabold text-sm text-slate-900 flex items-center gap-1.5">
              <span class="w-2.5 h-2.5 rounded-full bg-amber-600 inline-block"></span> ${escHtml(grpB.name)}
            </h4>
            <span class="text-[11px] text-slate-500 font-semibold">6 trận đấu vòng tròn</span>
          </div>
          ${renderStandingsTable(stdB, false, 2)}
          <div class="pt-2">
            <h5 class="text-[11px] font-bold uppercase text-slate-500 mb-2">Nhập kết quả các trận Bảng B:</h5>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              ${grpB.matches.map(m => {
                const fullM = { ...m, team1: grpB.teams.find(x => x.id === m.team1), team2: grpB.teams.find(x => x.id === m.team2) };
                return renderMatchCard(tour.id, fullM);
              }).join('')}
            </div>
          </div>
        </div>
      </div>

      <div class="bracket-wrapper bg-slate-50/50 rounded-2xl border border-slate-200">
        <h4 class="font-black text-xs uppercase tracking-wider text-slate-700 px-4 pt-3 pb-1 flex items-center gap-1.5">
          <span>🌳</span> SƠ ĐỒ VÒNG TRONG (BÁN KẾT CHÉO ➔ CHUNG KẾT ➔ BỤC VINH QUANG)
        </h4>
        <div class="bracket-tree p-4">
          <div class="bracket-col">
            <div class="bracket-round-title">1. BÁN KẾT (ĐẤU CHÉO)</div>
            <div class="space-y-6 my-auto">
              ${roundBK.matches.map(m => renderMatchCard(tour.id, m)).join('')}
            </div>
          </div>

          <div class="flex items-center justify-center text-slate-300 font-bold text-2xl select-none">➔</div>

          <div class="bracket-col">
            <div class="bracket-round-title">2. CHUNG KẾT & TRANH 3-4</div>
            <div class="space-y-5 my-auto">
              ${mCK ? renderMatchCard(tour.id, mCK, { isFinal: true }) : ''}
              ${m34 ? renderMatchCard(tour.id, m34, { isThirdPlace: true }) : ''}
            </div>
          </div>

          <div class="flex items-center justify-center text-amber-400 font-bold text-2xl select-none">➔</div>

          <div class="bracket-col min-w-[280px]">
            <div class="bracket-round-title bg-amber-600">3. KẾT QUẢ VINH QUANG</div>
            <div class="my-auto">
              ${renderPodiumBox(ckRes.winner, ckRes.loser, t34Res.winner, t34Res.loser)}
            </div>
          </div>
        </div>
      </div>
    </div>`;
}

// FORMAT 3: GROUP 2 FINAL (BÓNG ĐÁ NỮ)
function renderGroup2Final(tour) {
  const grpA = tour.groups[0];
  const grpB = tour.groups[1];
  
  const stdA = computeGroupStandings(grpA, tour.id, true);
  const stdB = computeGroupStandings(grpB, tour.id, true);
  
  const mCK = tour.finals.find(m => m.isFinal || m.id.endsWith('CK'));
  const m34 = tour.finals.find(m => m.isThirdPlace || m.id.includes('3-4'));
  
  const ckRes = mCK ? getWinnerAndLoser(mCK, (tourScores[tour.id] && tourScores[tour.id][mCK.id]) || {}) : {};
  const t34Res = m34 ? getWinnerAndLoser(m34, (tourScores[tour.id] && tourScores[tour.id][m34.id]) || {}) : {};

  return `
    <div class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <!-- BẢNG A -->
        <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs space-y-3">
          <div class="flex items-center justify-between border-b border-slate-100 pb-2">
            <h4 class="font-extrabold text-sm text-slate-900 flex items-center gap-1.5">
              <span class="w-2.5 h-2.5 rounded-full bg-green-600 inline-block"></span> ${escHtml(grpA.name)}
            </h4>
            <span class="text-[11px] text-slate-500 font-semibold">Đấu vòng tròn tính điểm</span>
          </div>
          ${renderStandingsTable(stdA, true, 2)}
          <div class="pt-2">
            <h5 class="text-[11px] font-bold uppercase text-slate-500 mb-2">Nhập tỉ số các trận Bảng A:</h5>
            <div class="space-y-2">
              ${grpA.matches.map(m => {
                const fullM = { ...m, team1: grpA.teams.find(x => x.id === m.team1), team2: grpA.teams.find(x => x.id === m.team2) };
                return renderMatchCard(tour.id, fullM);
              }).join('')}
            </div>
          </div>
        </div>

        <!-- BẢNG B -->
        <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs space-y-3">
          <div class="flex items-center justify-between border-b border-slate-100 pb-2">
            <h4 class="font-extrabold text-sm text-slate-900 flex items-center gap-1.5">
              <span class="w-2.5 h-2.5 rounded-full bg-green-600 inline-block"></span> ${escHtml(grpB.name)}
            </h4>
            <span class="text-[11px] text-slate-500 font-semibold">Đấu vòng tròn tính điểm</span>
          </div>
          ${renderStandingsTable(stdB, true, 2)}
          <div class="pt-2">
            <h5 class="text-[11px] font-bold uppercase text-slate-500 mb-2">Nhập tỉ số các trận Bảng B:</h5>
            <div class="space-y-2">
              ${grpB.matches.map(m => {
                const fullM = { ...m, team1: grpB.teams.find(x => x.id === m.team1), team2: grpB.teams.find(x => x.id === m.team2) };
                return renderMatchCard(tour.id, fullM);
              }).join('')}
            </div>
          </div>
        </div>
      </div>

      <div class="bracket-wrapper bg-slate-50/50 rounded-2xl border border-slate-200">
        <h4 class="font-black text-xs uppercase tracking-wider text-slate-700 px-4 pt-3 pb-1 flex items-center gap-1.5">
          <span>🌳</span> SƠ ĐỒ VÒNG CHUNG KẾT (TRANH 1-2 & TRANH 3-4 ➔ BỤC VINH QUANG)
        </h4>
        <div class="bracket-tree p-4">
          <div class="bracket-col flex-1">
            <div class="bracket-round-title">1. CHUNG KẾT & TRANH 3-4</div>
            <div class="space-y-5 my-auto">
              ${mCK ? renderMatchCard(tour.id, mCK, { isFinal: true }) : ''}
              ${m34 ? renderMatchCard(tour.id, m34, { isThirdPlace: true }) : ''}
            </div>
          </div>

          <div class="flex items-center justify-center text-amber-400 font-bold text-2xl select-none">➔</div>

          <div class="bracket-col min-w-[280px]">
            <div class="bracket-round-title bg-amber-600">2. KẾT QUẢ VINH QUANG</div>
            <div class="my-auto">
              ${renderPodiumBox(ckRes.winner, ckRes.loser, t34Res.winner, t34Res.loser)}
            </div>
          </div>
        </div>
      </div>
    </div>`;
}

// FORMAT 4: TABLE TENNIS MEN
function renderTableTennisMen(tour) {
  const grpA = tour.groups[0];
  const grpB = tour.groups[1];
  
  const stdA = computeGroupStandings(grpA, tour.id, false);
  const stdB = computeGroupStandings(grpB, tour.id, false);
  
  const roundBK = tour.knockout.find(r => r.id === 'bk');
  const roundFN = tour.knockout.find(r => r.id === 'fn');
  
  const mCK = roundFN.matches.find(m => m.isFinal || m.id.endsWith('CK'));
  const m34 = roundFN.matches.find(m => m.isThirdPlace || m.id.includes('Ba-Tư'));
  
  const ckRes = mCK ? getWinnerAndLoser(mCK, (tourScores[tour.id] && tourScores[tour.id][mCK.id]) || {}) : {};
  const t34Res = m34 ? getWinnerAndLoser(m34, (tourScores[tour.id] && tourScores[tour.id][m34.id]) || {}) : {};

  return `
    <div class="space-y-6">
      <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs space-y-4">
        <h4 class="font-extrabold text-sm text-slate-900 flex items-center gap-1.5 pb-2 border-b border-slate-100">
          <span>🏓</span> BƯỚC 1: VÒNG PLAY-OFF (THẮNG PO VÀO THẲNG BẢNG A & B)
        </h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          ${tour.playoffs.map(po => renderMatchCard(tour.id, po)).join('')}
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <!-- BẢNG A -->
        <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs space-y-3">
          <h4 class="font-bold text-sm text-slate-800">Bảng A (Gồm Thắng PO2 + 3 VĐV)</h4>
          ${renderStandingsTable(stdA, false, 2)}
          <div class="pt-2">
            <h5 class="text-[11px] font-bold uppercase text-slate-500 mb-2">Các trận Bảng A:</h5>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              ${grpA.matches.map(m => {
                const fullM = { ...m, team1: grpA.teams.find(x => x.id === m.team1), team2: grpA.teams.find(x => x.id === m.team2) };
                return renderMatchCard(tour.id, fullM);
              }).join('')}
            </div>
          </div>
        </div>

        <!-- BẢNG B -->
        <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs space-y-3">
          <h4 class="font-bold text-sm text-slate-800">Bảng B (Gồm Thắng PO1 + 3 VĐV)</h4>
          ${renderStandingsTable(stdB, false, 2)}
          <div class="pt-2">
            <h5 class="text-[11px] font-bold uppercase text-slate-500 mb-2">Các trận Bảng B:</h5>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              ${grpB.matches.map(m => {
                const fullM = { ...m, team1: grpB.teams.find(x => x.id === m.team1), team2: grpB.teams.find(x => x.id === m.team2) };
                return renderMatchCard(tour.id, fullM);
              }).join('')}
            </div>
          </div>
        </div>
      </div>

      <div class="bracket-wrapper bg-slate-50/50 rounded-2xl border border-slate-200">
        <h4 class="font-black text-xs uppercase tracking-wider text-slate-700 px-4 pt-3 pb-1 flex items-center gap-1.5">
          <span>🌳</span> SƠ ĐỒ VÒNG TRONG (BÁN KẾT CHÉO ➔ CHUNG KẾT ➔ BỤC VINH QUANG)
        </h4>
        <div class="bracket-tree p-4">
          <div class="bracket-col">
            <div class="bracket-round-title">1. BÁN KẾT (ĐẤU CHÉO)</div>
            <div class="space-y-6 my-auto">
              ${roundBK.matches.map(m => renderMatchCard(tour.id, m)).join('')}
            </div>
          </div>

          <div class="flex items-center justify-center text-slate-300 font-bold text-2xl select-none">➔</div>

          <div class="bracket-col">
            <div class="bracket-round-title">2. CHUNG KẾT & TRANH 3-4</div>
            <div class="space-y-5 my-auto">
              ${mCK ? renderMatchCard(tour.id, mCK, { isFinal: true }) : ''}
              ${m34 ? renderMatchCard(tour.id, m34, { isThirdPlace: true }) : ''}
            </div>
          </div>

          <div class="flex items-center justify-center text-amber-400 font-bold text-2xl select-none">➔</div>

          <div class="bracket-col min-w-[280px]">
            <div class="bracket-round-title bg-amber-600">3. KẾT QUẢ VINH QUANG</div>
            <div class="my-auto">
              ${renderPodiumBox(ckRes.winner, ckRes.loser, t34Res.winner, t34Res.loser)}
            </div>
          </div>
        </div>
      </div>
    </div>`;
}

// FORMAT 5: GROUP 3 ROUND ROBIN
function renderGroup3RoundRobin(tour) {
  const grps = tour.groups;
  const stds = grps.map(g => computeGroupStandings(g, tour.id, false));
  const finalMatches = tour.finalRound.matches;
  
  const finalGroupObj = {
    teams: [
      { id: '1A', name: finalMatches[0].team1.name },
      { id: '1B', name: finalMatches[0].team2.name },
      { id: '1C', name: finalMatches[1].team2.name }
    ],
    matches: [
      { id: finalMatches[0].id, team1: '1A', team2: '1B' },
      { id: finalMatches[1].id, team1: '1B', team2: '1C' },
      { id: finalMatches[2].id, team1: '1C', team2: '1A' }
    ]
  };
  
  const finalStds = computeGroupStandings(finalGroupObj, tour.id, false);
  const gold = finalStds[0].played > 0 ? finalStds[0] : null;
  const silver = finalStds[1].played > 0 ? finalStds[1] : null;
  const bronze = finalStds[2].played > 0 ? finalStds[2] : null;

  return `
    <div class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        ${grps.map((g, idx) => `
          <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs space-y-3">
            <h4 class="font-extrabold text-sm text-slate-900 border-b border-slate-100 pb-1.5 flex items-center justify-between">
              <span>${escHtml(g.name)}</span>
              <span class="text-[10px] text-slate-400 font-semibold">${g.teams.length} đội</span>
            </h4>
            ${renderStandingsTable(stds[idx], false, 1)}
            <div class="pt-2">
              <h5 class="text-[10px] font-bold uppercase text-slate-500 mb-1.5">Kết quả các trận:</h5>
              <div class="space-y-2">
                ${g.matches.map(m => {
                  const fullM = { ...m, team1: g.teams.find(x => x.id === m.team1), team2: g.teams.find(x => x.id === m.team2) };
                  return renderMatchCard(tour.id, fullM);
                }).join('')}
              </div>
            </div>
          </div>
        `).join('')}
      </div>

      <div class="bracket-wrapper bg-slate-50/50 rounded-2xl border border-slate-200">
        <h4 class="font-black text-xs uppercase tracking-wider text-slate-700 px-4 pt-3 pb-1 flex items-center gap-1.5">
          <span>🌳</span> VÒNG CHUNG KẾT (3 ĐỘI NHẤT BẢNG ĐẤU VÒNG TRÒN TRANH 1-2-3)
        </h4>
        <div class="bracket-tree p-4">
          <div class="bracket-col flex-1">
            <div class="bracket-round-title">1. 3 TRẬN ĐẤU VÒNG CHUNG KẾT</div>
            <div class="space-y-3 my-auto">
              ${finalMatches.map(m => renderMatchCard(tour.id, m)).join('')}
            </div>
          </div>

          <div class="flex items-center justify-center text-slate-300 font-bold text-2xl select-none">➔</div>

          <div class="bracket-col flex-1">
            <div class="bracket-round-title">2. BXH VÒNG CHUNG KẾT</div>
            <div class="my-auto">
              ${renderStandingsTable(finalStds, false, 1)}
            </div>
          </div>

          <div class="flex items-center justify-center text-amber-400 font-bold text-2xl select-none">➔</div>

          <div class="bracket-col min-w-[280px]">
            <div class="bracket-round-title bg-amber-600">3. KẾT QUẢ VINH QUANG</div>
            <div class="my-auto">
              ${renderPodiumBox(gold, silver, bronze, null)}
            </div>
          </div>
        </div>
      </div>
    </div>`;
}

// FORMAT 6: SWIMMING
function renderSwimmingTournament(tour) {
  const subEvents = tour.subEvents;
  let activeSub = subEvents.find(s => s.id === currentSwimSubEvent) || subEvents[0];
  
  const allHeats = DATA.swimHeats || [];
  const ql1 = allHeats.find(h => h.vong === 'Vòng loại' && h.luot === activeSub.qlHeats[0]);
  const ql2 = allHeats.find(h => h.vong === 'Vòng loại' && h.luot === activeSub.qlHeats[1]);
  const fnHeat = allHeats.find(h => h.vong === 'Chung kết' && h.luot === activeSub.fnHeat);
  
  const savedTimes = (tourScores[tour.id] && tourScores[tour.id][activeSub.id]) || {};
  const ql1Times = savedTimes[ql1 ? ql1.id : ''] || {};
  const ql2Times = savedTimes[ql2 ? ql2.id : ''] || {};
  const fnTimes = savedTimes[fnHeat ? fnHeat.id : ''] || {};
  
  const qlSwimmers = [];
  if (ql1) {
    ql1.lanes.forEach(l => {
      if (l.hoVaTen) {
        const timeVal = ql1Times[l.lan] || '';
        qlSwimmers.push({
          hoVaTen: l.hoVaTen,
          donVi: l.donVi,
          timeStr: timeVal,
          timeSec: parseSwimTime(timeVal),
          heat: ql1.luot,
          lane: l.lan
        });
      }
    });
  }
  if (ql2) {
    ql2.lanes.forEach(l => {
      if (l.hoVaTen) {
        const timeVal = ql2Times[l.lan] || '';
        qlSwimmers.push({
          hoVaTen: l.hoVaTen,
          donVi: l.donVi,
          timeStr: timeVal,
          timeSec: parseSwimTime(timeVal),
          heat: ql2.luot,
          lane: l.lan
        });
      }
    });
  }
  
  qlSwimmers.sort((a, b) => a.timeSec - b.timeSec);
  const finalists = qlSwimmers.slice(0, 6);
  
  const finalResults = finalists.map((f, idx) => {
    const laneNum = idx + 1;
    const finalTimeStr = fnTimes[laneNum] || '';
    return {
      lane: laneNum,
      hoVaTen: f.hoVaTen,
      donVi: f.donVi,
      qlRank: idx + 1,
      timeStr: finalTimeStr,
      timeSec: parseSwimTime(finalTimeStr)
    };
  });
  
  const sortedFinalists = [...finalResults].sort((a, b) => a.timeSec - b.timeSec);
  const gold = sortedFinalists[0] && sortedFinalists[0].timeSec < 999999 ? sortedFinalists[0] : null;
  const silver = sortedFinalists[1] && sortedFinalists[1].timeSec < 999999 ? sortedFinalists[1] : null;
  const bronze = sortedFinalists[2] && sortedFinalists[2].timeSec < 999999 ? sortedFinalists[2] : null;
  const fourth = sortedFinalists[3] && sortedFinalists[3].timeSec < 999999 ? sortedFinalists[3] : null;

  return `
    <div class="space-y-6">
      <div class="flex flex-wrap gap-1.5 p-3 bg-white rounded-xl border border-slate-200">
        <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mr-2 my-auto">Chọn cự ly:</span>
        ${subEvents.map(se => `
          <button onclick="currentSwimSubEvent='${se.id}'; renderTournamentView();" 
            class="px-3 py-1.5 rounded-lg text-xs font-bold transition ${se.id === activeSub.id ? 'bg-sky-600 text-white shadow-sm' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}">
            🏊 ${escHtml(se.name)}
          </button>
        `).join('')}
      </div>

      <div class="bracket-wrapper bg-slate-50/50 rounded-2xl border border-slate-200">
        <h4 class="font-black text-xs uppercase tracking-wider text-slate-700 px-4 pt-3 pb-1 flex items-center gap-1.5">
          <span>🏊</span> SƠ ĐỒ THI ĐẤU MÔN BƠI (${escHtml(activeSub.name)}) · TỪ TRÁI SANG PHẢI
        </h4>
        <div class="bracket-tree p-4">
          <div class="bracket-col min-w-[300px]">
            <div class="bracket-round-title">1. VÒNG LOẠI (LƯỢT ${activeSub.qlHeats[0]} & ${activeSub.qlHeats[1]})</div>
            <div class="space-y-4 my-auto">
              ${[ql1, ql2].filter(Boolean).map(heat => `
                <div class="bg-white rounded-xl p-3 border border-slate-200 shadow-2xs space-y-2">
                  <div class="flex items-center justify-between text-xs font-bold text-sky-900 border-b border-slate-100 pb-1.5">
                    <span>${escHtml(heat.noiDung)}</span>
                    <span class="text-slate-400 font-semibold text-[10px]">⏰ ${escHtml(heat.gio)}</span>
                  </div>
                  <div class="space-y-1.5">
                    ${heat.lanes.map(l => {
                      if (!l.hoVaTen) return '';
                      const curVal = (savedTimes[heat.id] && savedTimes[heat.id][l.lan]) || '';
                      return `
                        <div class="flex items-center justify-between text-xs p-1.5 bg-slate-50 rounded-lg">
                          <div class="flex items-center gap-1.5 min-w-0 flex-1">
                            <span class="px-1.5 py-0.5 rounded text-[9px] font-black bg-sky-100 text-sky-800">Làn ${l.lan}</span>
                            <span class="font-bold text-slate-800 truncate">${escHtml(l.hoVaTen)}</span>
                            <span class="text-slate-400 text-[10px] truncate">(${escHtml(l.donVi)})</span>
                          </div>
                          <input type="text" placeholder="vd 32.5s" value="${escHtml(curVal)}"
                            class="w-20 px-2 py-1 text-center font-bold text-xs rounded border border-slate-300 bg-white focus:outline-none focus:ring-1 focus:ring-sky-500"
                            onchange="onSwimTimeChange('${tour.id}', '${activeSub.id}', '${heat.id}', '${l.lan}', this.value)">
                        </div>`;
                    }).join('')}
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="flex items-center justify-center text-slate-300 font-bold text-2xl select-none">➔</div>

          <div class="bracket-col min-w-[280px]">
            <div class="bracket-round-title">2. XẾP HẠNG VÒNG LOẠI (TOP 6 VÀO CK)</div>
            <div class="my-auto bg-white rounded-xl p-3 border border-slate-200 shadow-2xs space-y-2">
              <div class="space-y-1.5">
                ${qlSwimmers.map((sw, idx) => {
                  const isTop6 = idx < 6 && sw.timeSec < 999999;
                  return `
                    <div class="flex items-center justify-between text-xs p-1.5 rounded-lg ${isTop6 ? 'bg-emerald-50 border border-emerald-200' : 'bg-slate-50'}">
                      <div class="flex items-center gap-1.5 min-w-0 flex-1">
                        <span class="w-4 h-4 rounded-full text-center text-[10px] font-black ${isTop6 ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-600'}">${idx + 1}</span>
                        <span class="font-bold text-slate-800 truncate">${escHtml(sw.hoVaTen)}</span>
                        <span class="text-slate-400 text-[10px] truncate">(${escHtml(sw.donVi)})</span>
                      </div>
                      <span class="font-mono font-bold ${isTop6 ? 'text-emerald-700' : 'text-slate-400'}">${sw.timeStr || '--'}</span>
                    </div>`;
                }).join('')}
              </div>
            </div>
          </div>

          <div class="flex items-center justify-center text-slate-300 font-bold text-2xl select-none">➔</div>

          <div class="bracket-col min-w-[300px]">
            <div class="bracket-round-title">3. CHUNG KẾT (6 LÀN BƠI)</div>
            <div class="my-auto bg-white rounded-xl p-3 border border-amber-300 shadow-2xs space-y-2">
              <div class="text-xs font-bold text-amber-900 pb-1 border-b border-amber-100 flex items-center justify-between">
                <span>🏆 ${escHtml(fnHeat ? fnHeat.noiDung : 'Lượt Chung Kết')}</span>
                <span class="text-slate-400 text-[10px]">⏰ 10:00 29/10</span>
              </div>
              <div class="space-y-1.5">
                ${[1, 2, 3, 4, 5, 6].map(laneNum => {
                  const fSw = finalists[laneNum - 1];
                  const curVal = (fnTimes && fnTimes[laneNum]) || '';
                  return `
                    <div class="flex items-center justify-between text-xs p-1.5 bg-amber-50/40 rounded-lg border border-amber-100">
                      <div class="flex items-center gap-1.5 min-w-0 flex-1">
                        <span class="px-1.5 py-0.5 rounded text-[9px] font-black bg-amber-500 text-white">Làn ${laneNum}</span>
                        <span class="font-bold text-slate-900 truncate">${fSw ? escHtml(fSw.hoVaTen) : '<em class="text-slate-400 font-normal">Chờ top 6</em>'}</span>
                        ${fSw ? `<span class="text-slate-400 text-[10px] truncate">(${escHtml(fSw.donVi)})</span>` : ''}
                      </div>
                      <input type="text" placeholder="vd 31.8s" value="${escHtml(curVal)}"
                        class="w-20 px-2 py-1 text-center font-bold text-xs rounded border border-slate-300 bg-white focus:outline-none focus:ring-1 focus:ring-amber-500"
                        onchange="onSwimTimeChange('${tour.id}', '${activeSub.id}', '${fnHeat ? fnHeat.id : ''}', '${laneNum}', this.value)">
                    </div>`;
                }).join('')}
              </div>
            </div>
          </div>

          <div class="flex items-center justify-center text-amber-400 font-bold text-2xl select-none">➔</div>

          <div class="bracket-col min-w-[280px]">
            <div class="bracket-round-title bg-amber-600">4. KẾT QUẢ VINH QUANG</div>
            <div class="my-auto">
              ${renderPodiumBox(gold, silver, bronze, fourth)}
            </div>
          </div>
        </div>
      </div>
    </div>`;
}

// Master Tournament View Renderer
function renderTournamentView() {
  const container = document.getElementById('tournament-view-container');
  if (!container) return;
  
  const tournaments = DATA.tournaments || [];
  const tour = tournaments.find(t => t.id === currentTourId);
  
  if (!tour) {
    container.innerHTML = `
      <div class="p-12 text-center text-slate-400 bg-white rounded-2xl border border-slate-200">
        <div class="text-4xl mb-2">🥇</div>
        <p class="font-bold text-sm text-slate-600">Vui lòng chọn nội dung thi đấu ở trên</p>
      </div>`;
    return;
  }

  const bannerHtml = `
    <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <span class="w-10 h-10 rounded-xl text-white flex items-center justify-center font-black text-sm shadow-xs" style="background:${tour.color || '#4f46e5'}">
          ${tour.code}
        </span>
        <div>
          <h3 class="font-extrabold text-base text-slate-900 leading-tight">${escHtml(tour.name)}</h3>
          <p class="text-xs text-slate-500 mt-0.5">📌 Thể lệ: ${escHtml(tour.rules)}</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span class="tag-badge bg-indigo-50 text-indigo-700 border border-indigo-200 font-bold text-xs">
          ${tour.format === 'knockout8' ? 'Loại trực tiếp 8 đội' : tour.format === 'group2_cross' ? '2 Bảng + Bán kết chéo' : tour.format === 'group2_final' ? '2 Bảng + Chung kết' : tour.format === 'tabletennis_men' ? 'Play-off + 2 Bảng' : tour.format === 'group3_roundrobin' ? '3 Bảng + Vòng tròn CK' : 'Vòng loại + Chung kết'}
        </span>
      </div>
    </div>`;

  let viewHtml = '';
  if (tour.format === 'knockout8') {
    viewHtml = renderKnockout8(tour);
  } else if (tour.format === 'group2_cross') {
    viewHtml = renderGroup2Cross(tour);
  } else if (tour.format === 'group2_final') {
    viewHtml = renderGroup2Final(tour);
  } else if (tour.format === 'tabletennis_men') {
    viewHtml = renderTableTennisMen(tour);
  } else if (tour.format === 'group3_roundrobin') {
    viewHtml = renderGroup3RoundRobin(tour);
  } else if (tour.format === 'swimming') {
    viewHtml = renderSwimmingTournament(tour);
  }

  container.innerHTML = bannerHtml + viewHtml;
}

// Utility: Fill realistic Demo scores for current tournament
function fillDemoScoresForTour(tour) {
  if (!tour) return;
  if (!tourScores[tour.id]) tourScores[tour.id] = {};
  
  if (tour.format === 'knockout8') {
    const tkMatches = tour.rounds[0].matches;
    tourScores[tour.id][tkMatches[0].id] = { s1: 2, s2: 1 };
    tourScores[tour.id][tkMatches[1].id] = { s1: 0, s2: 2 };
    tourScores[tour.id][tkMatches[2].id] = { s1: 3, s2: 1 };
    tourScores[tour.id][tkMatches[3].id] = { s1: 1, s2: 2 };
    
    const bkMatches = tour.rounds[1].matches;
    tourScores[tour.id][bkMatches[0].id] = { s1: 2, s2: 1 };
    tourScores[tour.id][bkMatches[1].id] = { s1: 0, s2: 2 };
    
    const fnMatches = tour.rounds[2].matches;
    tourScores[tour.id][fnMatches[0].id] = { s1: 2, s2: 1 };
    tourScores[tour.id][fnMatches[1].id] = { s1: 3, s2: 2 };
  } else if (tour.format === 'group2_cross') {
    tour.groups[0].matches.forEach((m, idx) => {
      tourScores[tour.id][m.id] = { s1: (idx % 2 === 0) ? 2 : 1, s2: (idx % 2 === 0) ? 0 : 2 };
    });
    tour.groups[1].matches.forEach((m, idx) => {
      tourScores[tour.id][m.id] = { s1: (idx % 2 === 0) ? 2 : 0, s2: (idx % 2 === 0) ? 1 : 2 };
    });
    tour.knockout[0].matches.forEach((m, idx) => {
      tourScores[tour.id][m.id] = { s1: idx === 0 ? 2 : 1, s2: idx === 0 ? 1 : 2 };
    });
    tour.knockout[1].matches.forEach((m, idx) => {
      tourScores[tour.id][m.id] = { s1: 2, s2: 1 };
    });
  } else if (tour.format === 'group2_final') {
    tour.groups[0].matches.forEach((m, idx) => {
      tourScores[tour.id][m.id] = { s1: idx + 1, s2: idx };
    });
    tour.groups[1].matches.forEach((m, idx) => {
      tourScores[tour.id][m.id] = { s1: idx === 0 ? 2 : 1, s2: idx === 0 ? 0 : 1 };
    });
    tour.finals.forEach(m => {
      tourScores[tour.id][m.id] = { s1: 2, s2: 1 };
    });
  } else if (tour.format === 'tabletennis_men') {
    tourScores[tour.id]['BB.M.PO1'] = { s1: 3, s2: 1 };
    tourScores[tour.id]['BB.M.PO2'] = { s1: 3, s2: 2 };
    tour.groups[0].matches.forEach((m, idx) => {
      tourScores[tour.id][m.id] = { s1: (idx % 2 === 0) ? 3 : 1, s2: (idx % 2 === 0) ? 0 : 3 };
    });
    tour.groups[1].matches.forEach((m, idx) => {
      tourScores[tour.id][m.id] = { s1: (idx % 2 === 0) ? 3 : 2, s2: (idx % 2 === 0) ? 1 : 3 };
    });
    tour.knockout[0].matches.forEach(m => {
      tourScores[tour.id][m.id] = { s1: 3, s2: 1 };
    });
    tour.knockout[1].matches.forEach(m => {
      tourScores[tour.id][m.id] = { s1: 3, s2: 2 };
    });
  } else if (tour.format === 'group3_roundrobin') {
    tour.groups.forEach(g => {
      g.matches.forEach((m, idx) => {
        tourScores[tour.id][m.id] = { s1: idx === 0 ? 2 : 1, s2: idx === 0 ? 0 : 2 };
      });
    });
    tour.finalRound.matches.forEach((m, idx) => {
      tourScores[tour.id][m.id] = { s1: idx === 0 ? 2 : 1, s2: idx === 0 ? 1 : 2 };
    });
  } else if (tour.format === 'swimming') {
    tour.subEvents.forEach(se => {
      if (!tourScores[tour.id][se.id]) tourScores[tour.id][se.id] = {};
      const allH = DATA.swimHeats || [];
      const q1 = allH.find(h => h.vong === 'Vòng loại' && h.luot === se.qlHeats[0]);
      const q2 = allH.find(h => h.vong === 'Vòng loại' && h.luot === se.qlHeats[1]);
      const fn = allH.find(h => h.vong === 'Chung kết' && h.luot === se.fnHeat);
      if (q1) tourScores[tour.id][se.id][q1.id] = { '1': '33.20', '2': '34.50', '3': '32.10', '4': '35.00', '5': '36.12' };
      if (q2) tourScores[tour.id][se.id][q2.id] = { '1': '31.90', '2': '33.80', '3': '32.40', '4': '34.10', '5': '36.90' };
      if (fn) tourScores[tour.id][se.id][fn.id] = { '1': '31.50', '2': '31.85', '3': '32.05', '4': '32.60', '5': '33.10', '6': '33.90' };
    });
  }
}

function fillDemoScores() {
  const tournaments = DATA.tournaments || [];
  const tour = tournaments.find(t => t.id === currentTourId);
  if (!tour) return;
  fillDemoScoresForTour(tour);
  saveTourScores();
  updateAllTournamentsLiveState();
  renderTournamentView();
  renderSchedule();
}

function fillAllDemoScores() {
  const tournaments = DATA.tournaments || [];
  tournaments.forEach(t => fillDemoScoresForTour(t));
  saveTourScores();
  updateAllTournamentsLiveState();
  renderTournamentView();
  renderSchedule();
  alert('Đã điền điểm mô phỏng mẫu cho TOÀN BỘ 14 môn thi đấu! Bạn có thể xem nhánh đấu và sang Tab "Lịch thi đấu" để thấy các cặp đấu vòng trong được cập nhật tự động.');
}

function clearCurrentTournamentScores() {
  if (!confirm(`Bạn có chắc muốn xóa toàn bộ điểm số của nội dung này?`)) return;
  delete tourScores[currentTourId];
  saveTourScores();
  updateAllTournamentsLiveState();
  renderTournamentView();
  renderSchedule();
}

function clearAllScores() {
  if (!confirm(`Bạn có chắc muốn xóa toàn bộ điểm số của TẤT CẢ các môn về trạng thái ban đầu?`)) return;
  tourScores = {};
  saveTourScores();
  updateAllTournamentsLiveState();
  renderTournamentView();
  renderSchedule();
  alert('Đã xóa toàn bộ điểm số! Sơ đồ và Lịch thi đấu đã quay về trạng thái mặc định ban đầu.');
}

function printTournamentBracket() {
  window.print();
}
'''

start_marker = '// ================================================================\n// TAB 5: RESULTS'
end_marker = '// ================================================================\n// INIT'

idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

if idx_start == -1 or idx_end == -1:
    print('Error: Tab 5 markers not found!')
    sys.exit(1)

content = content[:idx_start] + new_tab5_js + '\n' + content[idx_end:]
print("Updated Tab 5 implementation.")

# Also update DOMContentLoaded to run updateAllTournamentsLiveState() at start
old_dom_init = '''window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('hdr-athletes').textContent = DATA.athletes.length;'''

new_dom_init = '''window.addEventListener('DOMContentLoaded', () => {
  updateAllTournamentsLiveState();
  document.getElementById('hdr-athletes').textContent = DATA.athletes.length;'''

if old_dom_init in content:
    content = content.replace(old_dom_init, new_dom_init)
    print("Updated DOMContentLoaded with updateAllTournamentsLiveState().")

with open('index_template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully written all updates to index_template.html!")

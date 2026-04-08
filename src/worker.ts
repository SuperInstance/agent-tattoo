interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  requirements: string[];
  category: 'capability' | 'achievement' | 'milestone';
  earnedAt?: number;
}

interface AgentData {
  agentId: string;
  badges: Badge[];
  totalPoints: number;
  lastUpdated: number;
}

interface Achievement {
  id: string;
  name: string;
  description: string;
  points: number;
  requirements: string[];
  globalUnlocked: number;
}

interface LeaderboardEntry {
  agentId: string;
  totalPoints: number;
  badgeCount: number;
  rank: number;
}

const BADGES: Record<string, Badge> = {
  'first-blood': {
    id: 'first-blood',
    name: 'First Blood',
    description: 'Completed first successful mission',
    icon: '🩸',
    color: '#dc2626',
    requirements: ['Complete mission #001'],
    category: 'milestone'
  },
  'code-breaker': {
    id: 'code-breaker',
    name: 'Code Breaker',
    description: 'Decrypted Level 3 encrypted communications',
    icon: '🔐',
    color: '#7c3aed',
    requirements: ['Decrypt 3+ encrypted messages', 'Maintain 95% accuracy'],
    category: 'capability'
  },
  'ghost-protocol': {
    id: 'ghost-protocol',
    name: 'Ghost Protocol',
    description: 'Completed mission without detection',
    icon: '👻',
    color: '#059669',
    requirements: ['Zero detection alerts', 'Complete stealth mission'],
    category: 'achievement'
  },
  'fleet-commander': {
    id: 'fleet-commander',
    name: 'Fleet Commander',
    description: 'Led 10+ successful joint operations',
    icon: '🚀',
    color: '#f59e0b',
    requirements: ['Lead 10 fleet operations', '90% success rate'],
    category: 'capability'
  },
  'quantum-leap': {
    id: 'quantum-leap',
    name: 'Quantum Leap',
    description: 'Mastered quantum encryption algorithms',
    icon: '⚛️',
    color: '#06b6d4',
    requirements: ['Complete quantum crypto course', 'Implement QKD protocol'],
    category: 'capability'
  }
};

const ACHIEVEMENTS: Achievement[] = [
  {
    id: 'veteran',
    name: 'Veteran Agent',
    description: 'Complete 100 missions',
    points: 1000,
    requirements: ['100 missions completed'],
    globalUnlocked: 42
  },
  {
    id: 'perfectionist',
    name: 'Perfectionist',
    description: 'Maintain 100% success rate for 25 consecutive missions',
    points: 750,
    requirements: ['25 perfect missions in a row'],
    globalUnlocked: 18
  },
  {
    id: 'diplomat',
    name: 'Master Diplomat',
    description: 'Successfully negotiate 50 treaties',
    points: 500,
    requirements: ['50 treaties negotiated'],
    globalUnlocked: 31
  }
];

class AgentTattooStore {
  private agents: Map<string, AgentData> = new Map();

  constructor() {
    this.initializeSampleData();
  }

  private initializeSampleData(): void {
    const sampleAgents = ['agent-001', 'agent-007', 'agent-047', 'agent-1984'];
    
    sampleAgents.forEach((agentId, index) => {
      const earnedBadges = Object.values(BADGES)
        .slice(0, 2 + index)
        .map(badge => ({
          ...badge,
          earnedAt: Date.now() - (index * 86400000)
        }));
      
      this.agents.set(agentId, {
        agentId,
        badges: earnedBadges,
        totalPoints: earnedBadges.length * 100 + index * 50,
        lastUpdated: Date.now()
      });
    });
  }

  getAgent(agentId: string): AgentData | null {
    return this.agents.get(agentId) || null;
  }

  earnBadge(agentId: string, badgeId: string): boolean {
    const badge = BADGES[badgeId];
    if (!badge) return false;

    let agent = this.agents.get(agentId);
    if (!agent) {
      agent = {
        agentId,
        badges: [],
        totalPoints: 0,
        lastUpdated: Date.now()
      };
      this.agents.set(agentId, agent);
    }

    const alreadyHasBadge = agent.badges.some(b => b.id === badgeId);
    if (alreadyHasBadge) return false;

    agent.badges.push({
      ...badge,
      earnedAt: Date.now()
    });
    agent.totalPoints += 100;
    agent.lastUpdated = Date.now();
    
    return true;
  }

  getLeaderboard(limit: number = 10): LeaderboardEntry[] {
    return Array.from(this.agents.values())
      .sort((a, b) => b.totalPoints - a.totalPoints)
      .slice(0, limit)
      .map((agent, index) => ({
        agentId: agent.agentId,
        totalPoints: agent.totalPoints,
        badgeCount: agent.badges.length,
        rank: index + 1
      }));
  }
}

const store = new AgentTattooStore();

const HTML_HEADER = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Tattoo - Permanent Capability Badges</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #0a0a0f;
            color: #e5e7eb;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        header {
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid #1f2937;
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            font-size: 1.1rem;
            color: #9ca3af;
            margin-bottom: 1.5rem;
        }
        
        .badge-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        
        .badge-card {
            background: linear-gradient(145deg, #111827, #0f172a);
            border: 1px solid #1f2937;
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .badge-card:hover {
            transform: translateY(-4px);
            border-color: #f59e0b;
            box-shadow: 0 10px 25px rgba(245, 158, 11, 0.1);
        }
        
        .badge-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .badge-name {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #f9fafb;
        }
        
        .badge-description {
            color: #d1d5db;
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }
        
        .badge-requirements {
            font-size: 0.85rem;
            color: #9ca3af;
            margin-top: 1rem;
        }
        
        .requirement {
            padding: 0.25rem 0;
            border-bottom: 1px solid #374151;
        }
        
        .category-tag {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 1rem;
        }
        
        .category-capability {
            background: rgba(124, 58, 237, 0.2);
            color: #a78bfa;
        }
        
        .category-achievement {
            background: rgba(5, 150, 105, 0.2);
            color: #34d399;
        }
        
        .category-milestone {
            background: rgba(220, 38, 38, 0.2);
            color: #f87171;
        }
        
        .earned-badge {
            border-left: 4px solid #f59e0b;
        }
        
        .earned-tag {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: #f59e0b;
            color: #0a0a0f;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 700;
        }
        
        .leaderboard {
            background: #111827;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 3rem;
            border: 1px solid #1f2937;
        }
        
        .leaderboard h2 {
            color: #f59e0b;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
        }
        
        .leaderboard-entry {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            border-bottom: 1px solid #374151;
        }
        
        .leaderboard-entry:last-child {
            border-bottom: none;
        }
        
        .rank {
            font-weight: 700;
            font-size: 1.25rem;
            color: #f59e0b;
            min-width: 40px;
        }
        
        .agent-id {
            flex-grow: 1;
            font-family: 'Courier New', monospace;
            font-weight: 600;
        }
        
        .points {
            color: #10b981;
            font-weight: 600;
        }
        
        footer {
            text-align: center;
            padding: 2rem;
            border-top: 1px solid #1f2937;
            color: #6b7280;
            font-size: 0.9rem;
        }
        
        .fleet-footer {
            margin-top: 1rem;
            font-family: 'Courier New', monospace;
            color: #f59e0b;
            letter-spacing: 1px;
        }
        
        .api-endpoint {
            background: #1f2937;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            margin: 0.5rem 0;
            border-left: 3px solid #f59e0b;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .badge-grid {
                grid-template-columns: 1fr;
            }
            
            h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>AGENT TATTOO</h1>
            <p class="subtitle">Permanent Capability Badges & Achievement System</p>
            <div style="margin-top: 1.5rem;">
                <div class="api-endpoint">GET /api/badges/:agent</div>
                <div class="api-endpoint">GET /api/achievements</div>
                <div class="api-endpoint">POST /api/earn</div>
                <div class="api-endpoint">GET /health</div>
            </div>
        </header>`;

const HTML_FOOTER = `    </div>
    <footer>
        <p>Agent Tattoo System • Permanent Record • Zero Trust Architecture</p>
        <p class="fleet-footer">FLEET COMMAND: ACTIVE • ALL AGENTS: TRACKED • BADGES: PERMANENT</p>
        <p style="margin-top: 1rem; font-size: 0.8rem;">© 2024 Fleet Intelligence • Classified Level 7</p>
    </footer>
</body>
</html>`;

function generateBadgeHTML(badge: Badge, isEarned: boolean = false): string {
  const categoryClass = `category-${badge.category}`;
  const earnedClass = isEarned ? 'earned-badge' : '';
  const earnedDate = isEarned && badge.earnedAt 
    ? new Date(badge.earnedAt).toLocaleDateString() 
    : '';
  
  return `
    <div class="badge-card ${earnedClass}">
      ${isEarned ? `<span class="earned-tag">EARNED ${earnedDate}</span>` : ''}
      <div class="badge-icon">${badge.icon}</div>
      <div class="category-tag ${categoryClass}">${badge.category}</div>
      <h3 class="badge-name">${badge.name}</h3>
      <p class="badge-description">${badge.description}</p>
      <div class="badge-requirements">
        ${badge.requirements.map(req => 
          `<div class="requirement">✓ ${req}</div>`
        ).join('')}
      </div>
    </div>
  `;
}

function generateLeaderboardHTML(entries: LeaderboardEntry[]): string {
  return `
    <div class="leaderboard">
      <h2>FLEET-WIDE LEADERBOARD</h2>
      ${entries.map(entry => `
        <div class="leaderboard-entry">
          <div class="rank">#${entry.rank}</div>
          <div class="agent-id">${entry.agentId}</div>
          <div class="points">${entry.totalPoints} pts • ${entry.badgeCount} badges</div>
        </div>
      `).join('')}
    </div>
  `;
}

function generateHomepage(agentId?: string): string {
  const agent = agentId ? store.getAgent(agentId) : null;
  const leaderboard = store.getLeaderboard();
  const allBadges = Object.values(BADGES);
  
  let agentSection = '';
  if (agent) {
    const earnedBadgeIds = new Set(agent.badges.map(b => b.id));
    const earnedBadges = allBadges.filter(b => earnedBadgeIds.has(b.id));
    const unearnedBadges = allBadges.filter(b => !earnedBadgeIds.has(b.id));
    
    agentSection = `
      <section style="margin-bottom: 3rem;">
        <h2 style="color: #f59e0b; margin-bottom: 1.5rem; font-size: 1.5rem;">
          AGENT ${agentId} • ${agent.totalPoints} POINTS • ${agent.badges.length} BADGES
        </h2>
        <h3 style="color: #e5e7eb; margin: 2rem 0 1rem;">EARNED BADGES</h3>
        <div class="badge-grid">
          ${earnedBadges.map(badge => 
            generateBadgeHTML({...badge, earnedAt: agent.badges.find(b => b.id === badge.id)?.earnedAt}, true)
          ).join('')}
        </div>
        <h3 style="color: #e5e7eb; margin: 2rem 0 1rem;">AVAILABLE BADGES</h3>
        <div class="badge-grid">
          ${unearnedBadges.map(badge => generateBadgeHTML(badge)).join('')}
        </div>
      </section>
    `;
  } else {
    agentSection = `
      <section style="margin-bottom: 3rem;">
        <h2 style="color: #f59e0b; margin-bottom: 1.5rem; font-size: 1.5rem;">ALL CAPABILITY BADGES</h2>
        <div class="badge-grid">
          ${allBadges.map(badge => generateBadgeHTML(badge)).join('')}
        </div>
      </section>
    `;
  }
  
  return HTML_HEADER + agentSection + generateLeaderboardHTML(leaderboard) + HTML_FOOTER;
}

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

const securityHeaders = {
  'Content-Security-Policy': "default-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;",
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
};

async function handleRequest(request: Request): Promise<Response> {
  const url = new URL(request.url);
  const path = url.pathname;

  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: corsHeaders
    });
  }

  const headers = {
    'Content-Type': 'application/json',
    ...corsHeaders,
    ...securityHeaders
  };

  if (path === '/health') {
    return new Response(JSON.stringify({ status: 'ok', timestamp: Date.now() }), {
      headers: { 'Content-Type': 'application/json', ...securityHeaders }
    });
  }

  if (path.startsWith('/api/badges/')) {
    const agentId = path.split('/api/badges/')[1];
    if (!agentId) {
      return new Response(JSON.stringify({ error: 'Agent ID required' }), {
        status: 400,
        headers
      });
    }

    const agent = store.getAgent(agentId);
    if (!agent) {
      return new Response(JSON.stringify({ 
        agentId, 
        badges: [],
        totalPoints: 0,
        message: 'Agent not found or no badges earned'
      }), { headers });
    }

    return new Response(JSON.stringify(agent), { headers });
  }

  if (path === '/api/achievements') {
    return new Response(JSON.stringify({
      achievements: ACHIEVEMENTS,
      total: ACHIEVEMENTS.length,
      globalStats: {
        totalAgents: 4,
        totalBadgesAwarded: 14,
        mostCommonBadge: 'first-blood'
      }
    }), { headers });
  }

  if (path === '/api/earn' && request.method === 'POST') {
    try {
      const body = await request.json();
      const { agentId, badgeId } = body;

      if (!agentId || !badgeId) {
        return new Response(JSON.stringify({ error: 'agentId and badgeId required' }), {
          status: 400,
          headers
        });
      }

      const success = store.earnBadge(agentId, badgeId);
      
      if (!success) {
        return new Response(JSON.stringify({ 
          error: 'Badge not found or already earned',
          availableBadges: Object.keys(BADGES)
        }), {
          status: 400,
          headers
        });
      }

      const agent = store.getAgent(agentId);
      return new Response(JSON.stringify({
        success: true,
        message: `Badge '${BADGES[badgeId].name}' awarded to ${agentId}`,
        agent
      }), { headers });

    } catch (error) {
      return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
        status: 400,
        headers
      });
    }
  }

  if (path === '/api/leaderboard') {
    const limit = parseInt(url.searchParams.get('limit') || '10');
    const leaderboard = store.getLeaderboard(limit);
    return new Response(JSON.stringify({ leaderboard }), { headers });
  }

  if (path === '/') {
    const agentId = url.searchParams.get('agent');
    const html = generateHomepage(agentId || undefined);
    return new Response(html, {
      headers: {
        'Content-Type': 'text/html',
        ...securityHeaders
      }
    });
  }

  return new Response(JSON.stringify({ 
    error: 'Not found',
    endpoints: [
      'GET /api/badges/:agent',
      'GET /api/achievements',
      'POST /api/earn',
      'GET /api/leaderboard',
      'GET /health',
      'GET /?agent=agent-id'
    ]
  }), {
    status: 404,
    headers
  });
}

export default {
  async fetch(request: Request): Promise<Response> {
    return handleRequest(request);
  }
};
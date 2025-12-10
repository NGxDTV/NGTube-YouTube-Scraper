// NGTube Web Demo JavaScript - Retro Modern Edition

// Tab switching functionality
function showTab(tabName, event) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => button.classList.remove('active'));

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Add active class to clicked button - find the right button if no event
    if (event && event.target) {
        event.target.classList.add('active');
    } else {
        // Find button by tab name
        const btnIndex = {'video': 0, 'comments': 1, 'channel': 2, 'search': 3};
        if (btnIndex[tabName] !== undefined) {
            buttons[btnIndex[tabName]].classList.add('active');
        }
    }
}

// Open video info in Video tab
async function openVideoInfo(videoId) {
    const url = `https://www.youtube.com/watch?v=${videoId}`;
    document.getElementById('videoUrl').value = url;
    showTab('video');
    document.getElementById('videoForm').dispatchEvent(new Event('submit'));
}

// Open video comments in Comments tab
async function openVideoComments(videoId) {
    const url = `https://www.youtube.com/watch?v=${videoId}`;
    document.getElementById('commentsUrl').value = url;
    showTab('comments');
    document.getElementById('commentsForm').dispatchEvent(new Event('submit'));
}

// Form submission handlers
document.getElementById('videoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await submitForm('videoForm', 'videoResults', '/video', renderVideoInfo);
});

document.getElementById('commentsForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await submitForm('commentsForm', 'commentsResults', '/comments', renderComments);
});

// Store channel data globally for load more functionality
let currentChannelData = null;
let currentChannelUrl = null;
let currentLoadedVideos = 0;
let loadedVideoIds = new Set();

document.getElementById('channelForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    currentChannelData = null;
    currentLoadedVideos = 0;
    loadedVideoIds = new Set();
    currentChannelUrl = document.getElementById('channelUrl').value;
    await submitForm('channelForm', 'channelResults', '/channel', renderChannelInfo);
});

document.getElementById('searchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await submitForm('searchForm', 'searchResults', '/search', renderSearchResults);
});

// Generic form submission function
async function submitForm(formId, resultsId, endpoint, renderFunction) {
    const form = document.getElementById(formId);
    const resultsDiv = document.getElementById(resultsId);
    const formData = new FormData(form);

    // Show loading state with retro style
    resultsDiv.innerHTML = '<div class="loading">LOADING DATA...</div>';
    resultsDiv.classList.remove('error');

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            resultsDiv.innerHTML = renderFunction(data.data);
        } else {
            resultsDiv.innerHTML = `<div class="error">${data.error}</div>`;
            resultsDiv.classList.add('error');
        }
    } catch (error) {
        resultsDiv.innerHTML = `<div class="error">${error.message}</div>`;
        resultsDiv.classList.add('error');
    }
}

// Helper function to get best thumbnail
function getBestThumbnail(thumbnails, preferredWidth = 480) {
    if (!thumbnails || !Array.isArray(thumbnails) || thumbnails.length === 0) {
        return null;
    }
    // Sort by width and get closest to preferred
    const sorted = [...thumbnails].sort((a, b) => {
        const diffA = Math.abs((a.width || 0) - preferredWidth);
        const diffB = Math.abs((b.width || 0) - preferredWidth);
        return diffA - diffB;
    });
    return sorted[0]?.url || thumbnails[0]?.url || null;
}

// Render functions for different data types

function renderVideoInfo(data) {
    if (!data) return '<div class="error">No data received</div>';

    const tags = data.tags ? data.tags.slice(0, 10).map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('') : '';
    
    // Get thumbnail
    const thumbnail = getBestThumbnail(data.thumbnail, 720) || 
                      (data.video_id ? `https://i.ytimg.com/vi/${data.video_id}/hqdefault.jpg` : null);

    // Format duration
    const duration = data.duration || formatDuration(data.duration_seconds);

    return `
        <div class="video-card">
            <div class="video-thumbnail-container">
                ${thumbnail ? 
                    `<img src="${thumbnail}" alt="Video Thumbnail" class="video-thumbnail" onerror="this.parentElement.innerHTML='<div class=\\'no-thumbnail\\'></div>'">` : 
                    '<div class="no-thumbnail"></div>'
                }
                ${duration ? `<span class="video-duration-badge">${duration}</span>` : ''}
            </div>
            <div class="video-content">
                <div class="video-title">${escapeHtml(data.title || 'Unknown Title')}</div>
                <div class="video-stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">Views</div>
                        <div class="stat-value">${formatNumber(data.view_count || 0)}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Likes</div>
                        <div class="stat-value">${formatNumber(data.like_count || 0)}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Channel</div>
                        <div class="stat-value" style="font-size: 0.7rem;">${escapeHtml(data.channel_name || 'N/A')}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Upload</div>
                        <div class="stat-value" style="font-size: 0.7rem;">${data.upload_date || data.published_time_text || 'N/A'}</div>
                    </div>
                </div>
                ${data.description ? `<div class="video-description">${escapeHtml(data.description).substring(0, 500)}${data.description.length > 500 ? '...' : ''}</div>` : ''}
                ${tags ? `<div class="video-tags">${tags}</div>` : ''}
            </div>
        </div>
    `;
}

function renderComments(data) {
    if (!data || !data.comments || data.comments.length === 0) {
        return '<div class="error">No comments found</div>';
    }

    const commentsHtml = data.comments.map(comment => {
        const avatarUrl = comment.authorThumbnail || comment.author_thumbnail;
        const avatarHtml = avatarUrl ? 
            `<img src="${avatarUrl}" alt="" class="comment-avatar" onerror="this.outerHTML='<div class=\\'comment-avatar-placeholder\\'>${(comment.author || 'A')[0].toUpperCase()}</div>'">` :
            `<div class="comment-avatar-placeholder">${(comment.author || 'A')[0].toUpperCase()}</div>`;
        
        return `
            <div class="comment-card">
                <div class="comment-header">
                    ${avatarHtml}
                    <div class="comment-author">${escapeHtml(comment.author || 'Anonymous')}</div>
                </div>
                <div class="comment-text">${escapeHtml(comment.text || '')}</div>
                <div class="comment-meta">
                    ${comment.likeCount || comment.like_count ? `<span class="comment-likes">${formatNumber(comment.likeCount || comment.like_count)}</span>` : ''}
                    <span>${comment.publishedTimeText || comment.published_time_text || ''}</span>
                </div>
            </div>
        `;
    }).join('');

    return `
        <div class="comments-section">
            <h3>Comments (${data.comments.length})</h3>
            ${commentsHtml}
        </div>
    `;
}

function renderChannelInfo(data) {
    if (!data) return '<div class="error">No data received</div>';

    // Extract stats from data.stats if available
    const stats = data.stats || {};
    const subscriberCount = stats.subscribers || 0;
    const videoCount = stats.video_count || 0;
    const loadedVideosCount = stats.loaded_videos_count || 0;
    const loadedReelsCount = stats.loaded_reels_count || 0;
    const loadedPlaylistsCount = stats.loaded_playlists_count || 0;

    // Get channel avatar - might be in different places
    const channelAvatar = data.avatar?.[0]?.url || data.thumbnails?.[0]?.url || null;
    
    // Get channel banner - use the largest available
    const channelBanner = data.banner ? data.banner.reduce((best, current) => {
        return (!best || (current.width * current.height) > (best.width * best.height)) ? current : best;
    }, null)?.url : null;

    // Deduplicate videos by videoId
    const seenIds = new Set();
    const uniqueVideos = data.videos ? data.videos.filter(video => {
        if (!video.videoId) return true; // Keep videos without ID (shouldn't happen)
        if (seenIds.has(video.videoId)) return false;
        seenIds.add(video.videoId);
        return true;
    }) : [];

    // Render videos with thumbnails
    const videosHtml = uniqueVideos.map(video => {
        // Get video thumbnail
        const videoThumb = getBestThumbnail(video.thumbnails, 320) || 
                          (video.videoId ? `https://i.ytimg.com/vi/${video.videoId}/mqdefault.jpg` : null);
        
        // Parse view count
        let viewCount = 0;
        if (video.viewCountText) {
            const match = video.viewCountText.match(/([\d.,]+)/);
            if (match) {
                viewCount = parseInt(match[1].replace(/[.,]/g, ''));
            }
        } else if (video.view_count || video.views) {
            viewCount = video.view_count || video.views;
        }

        return `
            <div class="video-item">
                <div class="video-item-thumbnail">
                    ${videoThumb ? 
                        `<img src="${videoThumb}" alt="" onerror="this.parentElement.innerHTML='<div class=\\'no-thumbnail\\'></div>'">` :
                        '<div class="no-thumbnail"></div>'
                    }
                    ${video.lengthText || video.duration ? `<span class="video-item-duration">${video.lengthText || video.duration}</span>` : ''}
                </div>
                <div class="video-item-content">
                    <div class="video-item-title">${escapeHtml(video.title || 'Unknown Title')}</div>
                    <div class="video-item-meta">
                        <span>${formatNumber(viewCount)} views</span>
                        <span>${video.publishedTimeText || video.upload_date || ''}</span>
                    </div>
                    <div class="video-item-actions">
                        <button class="video-item-btn info-btn" onclick="openVideoInfo('${video.videoId}')">🎬 Info</button>
                        <button class="video-item-btn comments-btn" onclick="openVideoComments('${video.videoId}')">💬 Comments</button>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    // Render reels with thumbnails
    const reelsHtml = data.reels && data.reels.length > 0 ? data.reels.map(reel => {
        // Get reel thumbnail
        const reelThumb = getBestThumbnail(reel.thumbnails, 320) || 
                         (reel.videoId ? `https://i.ytimg.com/vi/${reel.videoId}/mqdefault.jpg` : null);
        
        return `
            <div class="video-item">
                <div class="video-item-thumbnail">
                    ${reelThumb ? 
                        `<img src="${reelThumb}" alt="" onerror="this.parentElement.innerHTML='<div class=\\'no-thumbnail\\'></div>'">` :
                        '<div class="no-thumbnail"></div>'
                    }
                    <span class="video-item-duration">REEL</span>
                </div>
                <div class="video-item-content">
                    <div class="video-item-title">${escapeHtml(reel.title || 'Unknown Title')}</div>
                    <div class="video-item-meta">
                        <span>${reel.viewCountText || '0 views'}</span>
                    </div>
                    <div class="video-item-actions">
                        <button class="video-item-btn info-btn" onclick="openVideoInfo('${reel.videoId}')">🎬 Info</button>
                    </div>
                </div>
            </div>
        `;
    }).join('') : '';

    // Render playlists with thumbnails
    const playlistsHtml = data.playlists && data.playlists.length > 0 ? data.playlists.map(playlist => {
        // Get playlist thumbnail
        const playlistThumb = getBestThumbnail(playlist.thumbnails, 320);
        
        return `
            <div class="video-item">
                <div class="video-item-thumbnail">
                    ${playlistThumb ? 
                        `<img src="${playlistThumb}" alt="" onerror="this.parentElement.innerHTML='<div class=\\'no-thumbnail\\'></div>'">` :
                        '<div class="no-thumbnail"></div>'
                    }
                    <span class="video-item-duration">PLAYLIST</span>
                </div>
                <div class="video-item-content">
                    <div class="video-item-title">${escapeHtml(playlist.title || 'Unknown Playlist')}</div>
                    <div class="video-item-meta">
                        <span>${playlist.videoCountText || '0 videos'}</span>
                    </div>
                    <div class="video-item-actions">
                        <button class="video-item-btn" onclick="window.open('https://www.youtube.com/playlist?list=${playlist.playlistId}', '_blank')">📺 Open</button>
                    </div>
                </div>
            </div>
        `;
    }).join('') : '';

    // Store data for load more BEFORE returning
    currentChannelData = data;
    currentLoadedVideos = uniqueVideos.length;
    
    // Store video IDs for duplicate check (use unique list)
    loadedVideoIds.clear(); // Clear first to avoid stale data
    uniqueVideos.forEach(v => {
        if (v.videoId) loadedVideoIds.add(v.videoId);
    });

    return `
        <div class="channel-header">
            ${channelBanner ? `<div class="channel-banner"><img src="${channelBanner}" alt="" onerror="this.parentElement.style.display='none'"></div>` : ''}
            ${channelAvatar ? `<img src="${channelAvatar}" alt="" class="channel-avatar" onerror="this.style.display='none'">` : ''}
            <div class="channel-name">${escapeHtml(data.title || data.channel_name || 'Unknown Channel')}</div>
            ${data.description ? `<div class="channel-description">${escapeHtml(data.description).substring(0, 300)}${data.description.length > 300 ? '...' : ''}</div>` : ''}
            <div class="channel-stats">
                <div class="channel-stat">
                    <div class="channel-stat-label">Subscribers</div>
                    <div class="channel-stat-value">${formatNumber(subscriberCount)}</div>
                </div>
                <div class="channel-stat">
                    <div class="channel-stat-label">Videos</div>
                    <div class="channel-stat-value">${formatNumber(videoCount)}</div>
                </div>
                <div class="channel-stat">
                    <div class="channel-stat-label">Loaded Videos</div>
                    <div class="channel-stat-value">${formatNumber(loadedVideosCount)}</div>
                </div>
                ${loadedReelsCount > 0 ? `
                <div class="channel-stat">
                    <div class="channel-stat-label">Loaded Reels</div>
                    <div class="channel-stat-value">${formatNumber(loadedReelsCount)}</div>
                </div>
                ` : ''}
                ${loadedPlaylistsCount > 0 ? `
                <div class="channel-stat">
                    <div class="channel-stat-label">Loaded Playlists</div>
                    <div class="channel-stat-value">${formatNumber(loadedPlaylistsCount)}</div>
                </div>
                ` : ''}
            </div>
        </div>
        ${videosHtml ? `
            <div class="videos-section-title">Recent Videos (${uniqueVideos.length})</div>
            <div class="videos-grid" id="channelVideosGrid">${videosHtml}</div>
            <div class="load-more-container">
                <button class="load-more-btn" onclick="loadMoreChannelVideos()" id="loadMoreBtn">+ Load More Videos</button>
            </div>
        ` : ''}
        ${reelsHtml ? `
            <div class="videos-section-title">Recent Reels (${data.reels.length})</div>
            <div class="videos-grid">${reelsHtml}</div>
        ` : ''}
        ${playlistsHtml ? `
            <div class="videos-section-title">Recent Playlists (${data.playlists.length})</div>
            <div class="videos-grid">${playlistsHtml}</div>
        ` : ''}
    `;
}

// Load more channel videos
async function loadMoreChannelVideos() {
    const btn = document.getElementById('loadMoreBtn');
    const grid = document.getElementById('channelVideosGrid');
    
    if (!currentChannelUrl || !btn || !grid) return;
    
    btn.textContent = 'LOADING...';
    btn.classList.add('loading');
    btn.disabled = true;
    
    try {
        const newMax = currentLoadedVideos + 10;
        const formData = new FormData();
        formData.append('url', currentChannelUrl);
        formData.append('max_videos', newMax);
        
        const response = await fetch('/channel', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success && result.data.videos) {
            // Get only truly new videos (not already loaded) using ID check
            const newVideos = result.data.videos.filter(video => {
                if (!video.videoId) return false;
                return !loadedVideoIds.has(video.videoId);
            });
            
            if (newVideos.length === 0) {
                btn.textContent = 'NO MORE VIDEOS';
                btn.disabled = true;
                return;
            }
            
            // Add new video IDs to the set
            newVideos.forEach(v => {
                if (v.videoId) loadedVideoIds.add(v.videoId);
            });
            
            // Render new videos
            const newHtml = newVideos.map(video => {
                const videoThumb = getBestThumbnail(video.thumbnails, 320) || 
                                  (video.videoId ? `https://i.ytimg.com/vi/${video.videoId}/mqdefault.jpg` : null);
                
                let viewCount = 0;
                if (video.viewCountText) {
                    const match = video.viewCountText.match(/([\d.,]+)/);
                    if (match) viewCount = parseInt(match[1].replace(/[.,]/g, ''));
                } else if (video.view_count || video.views) {
                    viewCount = video.view_count || video.views;
                }
                
                return `
                    <div class="video-item">
                        <div class="video-item-thumbnail">
                            ${videoThumb ? 
                                `<img src="${videoThumb}" alt="" onerror="this.parentElement.innerHTML='<div class=\\'no-thumbnail\\'></div>'">` :
                                '<div class="no-thumbnail"></div>'
                            }
                            ${video.lengthText || video.duration ? `<span class="video-item-duration">${video.lengthText || video.duration}</span>` : ''}
                        </div>
                        <div class="video-item-content">
                            <div class="video-item-title">${escapeHtml(video.title || 'Unknown Title')}</div>
                            <div class="video-item-meta">
                                <span>${formatNumber(viewCount)} views</span>
                                <span>${video.publishedTimeText || video.upload_date || ''}</span>
                            </div>
                            <div class="video-item-actions">
                                <button class="video-item-btn info-btn" onclick="openVideoInfo('${video.videoId}')">🎬 Info</button>
                                <button class="video-item-btn comments-btn" onclick="openVideoComments('${video.videoId}')">💬 Comments</button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            grid.insertAdjacentHTML('beforeend', newHtml);
            currentLoadedVideos = result.data.videos.length;
            currentChannelData = result.data;
            
            // Update section title
            const title = document.querySelector('.videos-section-title');
            if (title) title.innerHTML = `<span style="color: var(--neon-pink)">►</span> Recent Videos (${currentLoadedVideos})`;
            
            btn.textContent = '+ Load More Videos';
        } else {
            btn.textContent = 'ERROR - TRY AGAIN';
        }
    } catch (error) {
        btn.textContent = 'ERROR - TRY AGAIN';
        console.error('Load more error:', error);
    }
    
    btn.classList.remove('loading');
    btn.disabled = false;
}

function renderSearchResults(data) {
    if (!data || data.length === 0) {
        return '<div class="error">No search results found</div>';
    }

    const resultsHtml = data.map(item => {
        let type = 'Video';
        if (item.type === 'channel') type = 'Channel';
        else if (item.type === 'playlist') type = 'Playlist';
        else if (item.type === 'movie') type = 'Movie';

        // Get thumbnail
        const thumbnail = item.thumbnail || 
                          (item.videoId ? `https://i.ytimg.com/vi/${item.videoId}/mqdefault.jpg` : null);

        // Parse view count
        let viewCount = 0;
        if (item.viewCount) {
            const match = item.viewCount.match(/([\d.,]+)/);
            if (match) {
                viewCount = parseInt(match[1].replace(/[.,]/g, ''));
            }
        } else if (item.view_count) {
            viewCount = item.view_count;
        }

        return `
            <div class="search-item">
                <div class="search-item-thumbnail">
                    ${thumbnail ? 
                        `<img src="${thumbnail}" alt="" onerror="this.parentElement.innerHTML='<div class=\\'no-thumbnail\\'></div>'">` : 
                        '<div class="no-thumbnail"></div>'
                    }
                    ${item.length || item.duration ? `<span class="search-item-duration">${item.length || item.duration}</span>` : ''}
                </div>
                <div class="search-item-content">
                    <span class="search-item-type">${type}</span>
                    <div class="search-item-title">${escapeHtml(item.title || 'Unknown Title')}</div>
                    ${item.channel ? `<div class="search-item-channel">${escapeHtml(item.channel)}</div>` : ''}
                    ${item.description ? `<div class="search-item-description">${escapeHtml(item.description)}</div>` : ''}
                    <div class="search-item-meta">
                        ${viewCount ? `<span>${formatNumber(viewCount)} views</span>` : ''}
                        ${item.publishedTime || item.upload_date ? `<span>${item.publishedTime || item.upload_date}</span>` : ''}
                    </div>
                </div>
            </div>
        `;
    }).join('');

    return `
        <div class="search-results-grid">
            ${resultsHtml}
        </div>
    `;
}

// Utility functions

function formatNumber(num) {
    if (!num) return '0';
    if (typeof num === 'string') num = parseInt(num);
    if (isNaN(num)) return '0';
    if (num >= 1000000000) {
        return (num / 1000000000).toFixed(1) + 'B';
    } else if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatDuration(seconds) {
    if (!seconds) return null;
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hrs > 0) {
        return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize the first tab as active
document.addEventListener('DOMContentLoaded', () => {
    showTab('video');
});

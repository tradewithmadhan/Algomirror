// Socket.IO event handling for AlgoMirror (placeholder for future real-time features)
(function() {
    'use strict';
    
    // Socket connection status
    let socket = null;
    let isConnected = false;
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;
    
    // Initialize Socket.IO connection (when needed)
    function initSocket() {
        if (typeof io === 'undefined') {
            console.log('Socket.IO not available');
            return;
        }
        
        // Only initialize if user is authenticated
        const isAuthenticated = document.body.dataset.authenticated === 'true';
        if (!isAuthenticated) return;
        
        try {
            socket = io({
                transports: ['websocket', 'polling'],
                autoConnect: true,
                reconnection: true,
                reconnectionAttempts: maxReconnectAttempts,
                reconnectionDelay: 1000,
                reconnectionDelayMax: 5000,
                maxHttpBufferSize: 1e6,
                pingTimeout: 60000,
                pingInterval: 25000
            });
            
            setupSocketEvents();
            
        } catch (error) {
            console.error('Failed to initialize socket connection:', error);
        }
    }
    
    // Setup socket event listeners
    function setupSocketEvents() {
        if (!socket) return;
        
        // Connection events
        socket.on('connect', function() {
            isConnected = true;
            reconnectAttempts = 0;
            console.log('Socket connected:', socket.id);
            updateConnectionStatus(true);
            
            // Join user's room for personalized updates
            const userId = document.body.dataset.userId;
            if (userId) {
                socket.emit('join_user_room', { user_id: userId });
            }
        });
        
        socket.on('disconnect', function(reason) {
            isConnected = false;
            console.log('Socket disconnected:', reason);
            updateConnectionStatus(false);
        });
        
        socket.on('connect_error', function(error) {
            console.error('Socket connection error:', error);
            reconnectAttempts++;
            
            if (reconnectAttempts >= maxReconnectAttempts) {
                console.log('Max reconnection attempts reached');
                updateConnectionStatus(false, 'Connection failed');
            }
        });
        
        socket.on('reconnect', function(attemptNumber) {
            console.log('Socket reconnected after', attemptNumber, 'attempts');
            isConnected = true;
            updateConnectionStatus(true);
        });
        
        socket.on('reconnect_error', function(error) {
            console.error('Socket reconnection error:', error);
        });
        
        socket.on('reconnect_failed', function() {
            console.error('Socket reconnection failed');
            updateConnectionStatus(false, 'Reconnection failed');
        });
        
        // Custom events for real-time updates
        setupRealTimeEvents();
    }
    
    // Setup real-time event handlers
    function setupRealTimeEvents() {
        if (!socket) return;
        
        // Account status updates
        socket.on('account_status_update', function(data) {
            handleAccountStatusUpdate(data);
        });
        
        // Trade updates
        socket.on('trade_update', function(data) {
            handleTradeUpdate(data);
        });
        
        // Order updates
        socket.on('order_update', function(data) {
            handleOrderUpdate(data);
        });
        
        // Position updates
        socket.on('position_update', function(data) {
            handlePositionUpdate(data);
        });
        
        // Funds updates
        socket.on('funds_update', function(data) {
            handleFundsUpdate(data);
        });
        
        // System notifications
        socket.on('system_notification', function(data) {
            handleSystemNotification(data);
        });
        
        // Market data updates (if subscribed)
        socket.on('market_data', function(data) {
            handleMarketDataUpdate(data);
        });
    }
    
    // Handle account status updates
    function handleAccountStatusUpdate(data) {
        console.log('Account status update:', data);
        
        // Update account status indicators
        const accountCards = document.querySelectorAll(`[data-account-id="${data.account_id}"]`);
        accountCards.forEach(card => {
            const statusBadge = card.querySelector('.status-badge');
            if (statusBadge) {
                statusBadge.textContent = data.status;
                statusBadge.className = `badge badge-${getStatusColor(data.status)} status-badge`;
            }
        });
        
        // Show notification
        if (window.showToast) {
            const message = `Account "${data.account_name}" is now ${data.status}`;
            const type = data.status === 'connected' ? 'success' : 'warning';
            showToast(message, type);
        }
    }
    
    // Handle trade updates
    function handleTradeUpdate(data) {
        console.log('Trade update:', data);
        
        // Update tradebook if visible
        if (window.location.pathname.includes('/trading/tradebook')) {
            // Refresh tradebook data
            setTimeout(() => location.reload(), 1000);
        }
        
        // Show notification
        if (window.showToast) {
            const message = `Trade executed: ${data.symbol} ${data.action} ${data.quantity}`;
            showToast(message, 'success');
        }
        
        // Play alert sound if enabled
        playAlertSound();
    }
    
    // Handle order updates
    function handleOrderUpdate(data) {
        console.log('Order update:', data);
        
        // Update orderbook if visible
        if (window.location.pathname.includes('/trading/orderbook')) {
            // Refresh orderbook data
            setTimeout(() => location.reload(), 1000);
        }
        
        // Show notification for completed/cancelled orders
        if (data.status === 'complete' || data.status === 'cancelled') {
            if (window.showToast) {
                const message = `Order ${data.status}: ${data.symbol}`;
                const type = data.status === 'complete' ? 'success' : 'warning';
                showToast(message, type);
            }
        }
    }
    
    // Handle position updates
    function handlePositionUpdate(data) {
        console.log('Position update:', data);
        
        // Update positions page if visible
        if (window.location.pathname.includes('/trading/positions')) {
            // Refresh positions data
            setTimeout(() => location.reload(), 1000);
        }
    }
    
    // Handle funds updates
    function handleFundsUpdate(data) {
        console.log('Funds update:', data);
        
        // Update funds display if visible
        if (window.location.pathname.includes('/trading/funds')) {
            // Refresh funds data
            setTimeout(() => location.reload(), 1000);
        }
        
        // Update dashboard if visible
        if (window.location.pathname === '/' || window.location.pathname.includes('/dashboard')) {
            setTimeout(() => location.reload(), 1000);
        }
    }
    
    // Handle system notifications
    function handleSystemNotification(data) {
        console.log('System notification:', data);
        
        if (window.showToast) {
            showToast(data.message, data.type || 'info');
        }
        
        // Play alert sound for important notifications
        if (data.priority === 'high') {
            playAlertSound();
        }
    }
    
    // Handle market data updates
    function handleMarketDataUpdate(data) {
        // Update live prices, quotes, etc.
        console.log('Market data update:', data);
        
        // Update price elements with data-symbol attribute
        const priceElements = document.querySelectorAll(`[data-symbol="${data.symbol}"]`);
        priceElements.forEach(element => {
            if (element.classList.contains('ltp')) {
                element.textContent = data.ltp;
                
                // Add price change indicator
                if (data.change) {
                    element.classList.remove('text-success', 'text-error');
                    element.classList.add(data.change > 0 ? 'text-success' : 'text-error');
                }
            }
        });
    }
    
    // Update connection status indicator
    function updateConnectionStatus(connected, message = '') {
        const statusIndicator = document.querySelector('.connection-status');
        if (statusIndicator) {
            statusIndicator.classList.toggle('connected', connected);
            statusIndicator.classList.toggle('disconnected', !connected);
            statusIndicator.title = connected ? 'Connected' : (message || 'Disconnected');
        }
        
        // Update connection indicator in navbar if present
        const navIndicator = document.querySelector('.nav-connection-status');
        if (navIndicator) {
            navIndicator.classList.toggle('online', connected);
            navIndicator.classList.toggle('offline', !connected);
        }
    }
    
    // Get status color for badges
    function getStatusColor(status) {
        const colors = {
            'connected': 'success',
            'disconnected': 'error',
            'connecting': 'warning',
            'failed': 'error',
            'error': 'error'
        };
        return colors[status] || 'neutral';
    }
    
    // Play alert sound
    function playAlertSound() {
        const alertSound = document.getElementById('alert-sound');
        if (alertSound) {
            alertSound.play().catch(error => {
                console.log('Could not play alert sound:', error);
            });
        }
    }
    
    // Emit event to server
    function emitEvent(eventName, data) {
        if (socket && isConnected) {
            socket.emit(eventName, data);
        } else {
            console.warn('Socket not connected, cannot emit event:', eventName);
        }
    }
    
    // Subscribe to market data
    function subscribeToMarketData(symbols) {
        if (Array.isArray(symbols) && symbols.length > 0) {
            emitEvent('subscribe_market_data', { symbols: symbols });
        }
    }
    
    // Unsubscribe from market data
    function unsubscribeFromMarketData(symbols) {
        if (Array.isArray(symbols) && symbols.length > 0) {
            emitEvent('unsubscribe_market_data', { symbols: symbols });
        }
    }
    
    // Initialize when DOM is ready
    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }
    
    // Initialize socket connection
    ready(function() {
        // Only initialize socket in production or when explicitly enabled
        const enableSocket = document.body.dataset.enableSocket === 'true';
        const isDevelopment = window.location.hostname === 'localhost' || 
                            window.location.hostname === '127.0.0.1';
        
        if (enableSocket || !isDevelopment) {
            // Delay initialization to allow page to load
            setTimeout(initSocket, 1000);
        }
    });
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', function() {
        if (socket) {
            socket.disconnect();
        }
    });
    
    // Export for manual control
    window.AlgoMirrorSocket = {
        connect: initSocket,
        disconnect: function() {
            if (socket) socket.disconnect();
        },
        emit: emitEvent,
        subscribeToMarketData: subscribeToMarketData,
        unsubscribeFromMarketData: unsubscribeFromMarketData,
        isConnected: function() { return isConnected; }
    };
    
})();
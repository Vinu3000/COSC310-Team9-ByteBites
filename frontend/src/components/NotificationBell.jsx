import { useState, useEffect, useRef } from 'react'
import '../styles/NotificationBell.css'

function NotificationBell() {
  const [notifications, setNotifications] = useState([])
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const dropdownRef = useRef(null)

  const fetchNotifications = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/v1/notifications/')
      if (res.ok) {
        const data = await res.json()
        setNotifications(Array.isArray(data) ? data : [])
      }
    } catch (err) {
      // silently fail — notifications are non-critical
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchNotifications()
  }, [])

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const formatTime = (timestamp) => {
    try {
      return new Date(timestamp).toLocaleString([], {
        month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
      })
    } catch {
      return timestamp
    }
  }

  return (
    <div className="notif-bell" ref={dropdownRef}>
      <button
        className="notif-bell__btn"
        onClick={() => {
          setOpen(prev => !prev)
          if (!open) fetchNotifications()
        }}
        title="Notifications"
      >
        🔔
        {notifications.length > 0 && (
          <span className="notif-bell__badge">{notifications.length}</span>
        )}
      </button>

      {open && (
        <div className="notif-bell__dropdown">
          <div className="notif-bell__header">
            <span>Notifications</span>
            <button className="notif-bell__refresh" onClick={fetchNotifications} title="Refresh">↻</button>
          </div>

          {loading && <p className="notif-bell__empty">Loading...</p>}

          {!loading && notifications.length === 0 && (
            <p className="notif-bell__empty">No notifications yet.</p>
          )}

          {!loading && notifications.map(n => (
            <div key={n.id} className="notif-bell__item">
              <p className="notif-bell__message">{n.message}</p>
              <span className="notif-bell__meta">
                Order #{n.order_id} &middot; {formatTime(n.timestamp)}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default NotificationBell

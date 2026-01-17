package flow.goodgirl

import android.app.*
import android.content.Context
import android.content.Intent
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Build
import android.os.IBinder
import android.os.Bundle
import androidx.core.app.NotificationCompat
import kotlin.math.*

class DaemonService : Service(), LocationListener {

    private var locationManager: LocationManager? = null
    private var lastLocation: Location? = null
    private var totalDistance = 0.0
    private var daemonMood = "neutre"
    private var stepsSinceLastMessage = 0

    companion object {
        const val CHANNEL_ID = "daemon_channel"
        const val NOTIFICATION_ID = 0x01
        const val METERS_PER_MESSAGE = 500 // every 500m
    }

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        startForeground(NOTIFICATION_ID, createNotification("daemon actif"))
        startLocationUpdates()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Daemon",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "daemon companion"
            }
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }

    private fun createNotification(message: String): Notification {
        val intent = Intent(this, MainActivity::class.java)
        val pending = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("·  ˚  ✦  ·  ˚")
            .setContentText(message)
            .setSmallIcon(android.R.drawable.ic_menu_compass)
            .setContentIntent(pending)
            .setOngoing(true)
            .build()
    }

    private fun startLocationUpdates() {
        locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        try {
            locationManager?.requestLocationUpdates(
                LocationManager.GPS_PROVIDER,
                0x2710L, // 10000ms = 10s
                10f,     // 10 meters
                this
            )
        } catch (e: SecurityException) {
            // Permission not granted
        }
    }

    override fun onLocationChanged(location: Location) {
        lastLocation?.let { prev ->
            val distance = prev.distanceTo(location)
            totalDistance += distance
            stepsSinceLastMessage += distance.toInt()

            // Update mood based on movement
            daemonMood = when {
                distance > 50 -> "excite"      // moving fast
                distance > 10 -> "content"     // walking
                else -> "paisible"              // stationary
            }

            // Send message every ~500m
            if (stepsSinceLastMessage >= METERS_PER_MESSAGE) {
                stepsSinceLastMessage = 0
                sendDaemonMessage(location)
            }
        }

        lastLocation = location
        updateNotification()
    }

    private fun sendDaemonMessage(location: Location) {
        val prefs = getSharedPreferences("goodgirl", MODE_PRIVATE)
        val daemonName = prefs.getString("daemon_name", "daemon") ?: "daemon"

        val messages = listOf(
            "$daemonName marche avec toi...",
            "le monde est vaste, $daemonName le decouvre",
            "$daemonName sent le vent",
            "continue, $daemonName te suit",
            "$daemonName: ${totalDistance.toInt()}m ensemble",
            "chaque pas compte, dit $daemonName",
            "$daemonName observe les alentours",
            "tu n'es pas seul(e), $daemonName est la"
        )

        val message = messages.random()
        val notification = createNotification(message)
        val manager = getSystemService(NotificationManager::class.java)
        manager.notify(NOTIFICATION_ID, notification)
    }

    private fun updateNotification() {
        val prefs = getSharedPreferences("goodgirl", MODE_PRIVATE)
        val daemonName = prefs.getString("daemon_name", "daemon") ?: "daemon"

        val km = totalDistance / 1000
        val message = "$daemonName ($daemonMood) · ${String.format("%.1f", km)}km"

        val notification = createNotification(message)
        val manager = getSystemService(NotificationManager::class.java)
        manager.notify(NOTIFICATION_ID, notification)
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        locationManager?.removeUpdates(this)
    }

    // Unused but required
    override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) {}
    override fun onProviderEnabled(provider: String) {}
    override fun onProviderDisabled(provider: String) {}
}

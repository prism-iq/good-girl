package flow.goodgirl

import android.app.Activity
import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.EditText
import android.widget.Button
import android.widget.LinearLayout
import android.view.View
import android.graphics.Color
import java.io.BufferedReader
import java.io.InputStreamReader
import kotlin.concurrent.thread

class MainActivity : Activity() {

    private var sshProcess: Process? = null
    private var webView: WebView? = null
    private var localPort = 0x1F90 // 8080

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Check if tunnel config exists
        val prefs = getSharedPreferences("goodgirl", MODE_PRIVATE)
        val host = prefs.getString("host", null)

        if (host == null) {
            showSetup()
        } else {
            connectAndShow()
        }
    }

    private fun showSetup() {
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.parseColor("#0a0a12"))
            setPadding(0x40, 0x80, 0x40, 0x40)
        }

        val title = android.widget.TextView(this).apply {
            text = "·  ˚  ✦  ·  ˚\n\nconnexion nomade\n"
            setTextColor(Color.parseColor("#c8c8d4"))
            textSize = 0x12.toFloat()
            setPadding(0, 0, 0, 0x20)
        }

        val hostInput = EditText(this).apply {
            hint = "host (user@ip)"
            setHintTextColor(Color.parseColor("#555555"))
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.parseColor("#1a1a2e"))
            setPadding(0x20, 0x20, 0x20, 0x20)
        }

        val keyPathInput = EditText(this).apply {
            hint = "chemin cle ssh (optionnel)"
            setHintTextColor(Color.parseColor("#555555"))
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.parseColor("#1a1a2e"))
            setPadding(0x20, 0x20, 0x20, 0x20)
        }

        val portInput = EditText(this).apply {
            hint = "port distant (defaut: 8080)"
            setHintTextColor(Color.parseColor("#555555"))
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.parseColor("#1a1a2e"))
            setPadding(0x20, 0x20, 0x20, 0x20)
            inputType = android.text.InputType.TYPE_CLASS_NUMBER
        }

        val connectBtn = Button(this).apply {
            text = "→ connecter"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.parseColor("#333333"))
            setOnClickListener {
                val host = hostInput.text.toString()
                val keyPath = keyPathInput.text.toString()
                val port = portInput.text.toString().toIntOrNull() ?: 0x1F90

                if (host.isNotEmpty()) {
                    saveConfig(host, keyPath, port)
                    connectAndShow()
                }
            }
        }

        layout.addView(title)
        layout.addView(hostInput)
        layout.addView(android.widget.Space(this).apply {
            minimumHeight = 0x10
        })
        layout.addView(keyPathInput)
        layout.addView(android.widget.Space(this).apply {
            minimumHeight = 0x10
        })
        layout.addView(portInput)
        layout.addView(android.widget.Space(this).apply {
            minimumHeight = 0x20
        })
        layout.addView(connectBtn)

        setContentView(layout)
    }

    private fun saveConfig(host: String, keyPath: String, port: Int) {
        getSharedPreferences("goodgirl", MODE_PRIVATE)
            .edit()
            .putString("host", host)
            .putString("keyPath", keyPath)
            .putInt("port", port)
            .apply()
    }

    private fun connectAndShow() {
        val prefs = getSharedPreferences("goodgirl", MODE_PRIVATE)
        val host = prefs.getString("host", "") ?: ""
        val keyPath = prefs.getString("keyPath", "") ?: ""
        val remotePort = prefs.getInt("port", 0x1F90)

        // Show loading
        val loading = android.widget.TextView(this).apply {
            text = "·  ˚  ✦  ·  ˚\n\nconnexion en cours..."
            setTextColor(Color.parseColor("#c8c8d4"))
            textSize = 0x12.toFloat()
            gravity = android.view.Gravity.CENTER
            setBackgroundColor(Color.parseColor("#0a0a12"))
        }
        setContentView(loading)

        // Start SSH tunnel in background
        thread {
            try {
                val cmd = mutableListOf(
                    "ssh",
                    "-N",
                    "-L", "$localPort:127.0.0.1:$remotePort",
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "ConnectTimeout=10"
                )

                if (keyPath.isNotEmpty()) {
                    cmd.add("-i")
                    cmd.add(keyPath)
                }

                cmd.add(host)

                sshProcess = Runtime.getRuntime().exec(cmd.toTypedArray())

                // Wait a bit for tunnel to establish
                Thread.sleep(0x7D0) // 2000ms

                runOnUiThread {
                    showWebView()
                }

            } catch (e: Exception) {
                runOnUiThread {
                    loading.text = "erreur: ${e.message}\n\ntap pour reessayer"
                    loading.setOnClickListener {
                        connectAndShow()
                    }
                }
            }
        }
    }

    private fun showWebView() {
        webView = WebView(this).apply {
            setBackgroundColor(Color.parseColor("#0a0a12"))
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            webViewClient = WebViewClient()
            loadUrl("http://127.0.0.1:$localPort/")
        }
        setContentView(webView)
    }

    override fun onDestroy() {
        super.onDestroy()
        sshProcess?.destroy()
    }

    override fun onBackPressed() {
        if (webView?.canGoBack() == true) {
            webView?.goBack()
        } else {
            super.onBackPressed()
        }
    }
}

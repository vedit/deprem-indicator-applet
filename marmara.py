import os
import signal
import hashlib
import time
import requests
import rumps
from datetime import datetime
import logging
import traceback
import subprocess
import platform

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class MarmaraDepremApp(rumps.App):
    def __init__(self):
        try:
            super(MarmaraDepremApp, self).__init__("Deprem")
            self.menu = [
                rumps.MenuItem("Son Deprem", callback=self.last_eq_menu),
                rumps.MenuItem("Deprem İstatistikleri", callback=self.eq_stats_menu),
                None,  # Separator
                rumps.MenuItem("Bildirim Testi", callback=self.test_notification),
            ]
            self.update_thread = None
            self.check_notification_permissions()
            logger.info("Application initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize application: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def check_notification_permissions(self):
        """Check if the application has notification permissions"""
        try:
            # Try to send a test notification
            logger.info("Checking notification permissions...")
            self.send_notification(
                title="Bildirim Testi",
                subtitle="İzin Kontrolü",
                message="Bu bir test bildirimidir.",
                sound=False,
            )
            logger.info("Notification permissions check completed")
        except Exception as e:
            logger.error(f"Notification permissions check failed: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            self.show_permission_instructions()

    def show_permission_instructions(self):
        """Show instructions for enabling notifications"""
        instructions = """
        Bildirimlerin çalışması için lütfen şu adımları takip edin:
        
        1. Sistem Tercihleri'ni açın
        2. Bildirimler ve Odaklanma'ya tıklayın
        3. Python veya Terminal uygulamasını bulun
        4. Bildirimlere izin verin
        5. Bildirim stilini "Banner" veya "Uyarı" olarak ayarlayın
        """
        logger.warning("Notification permissions not properly set")
        rumps.alert("Bildirim İzinleri", instructions)

    def send_notification(self, title, subtitle, message, sound=True):
        """Send a notification using multiple methods"""
        try:
            logger.debug(
                f"Attempting to send notification: {title} - {subtitle} - {message}"
            )

            # Method 1: Using rumps notification
            try:
                logger.debug("Trying rumps notification...")
                rumps.notification(
                    title=title, subtitle=subtitle, message=message, sound=sound
                )
                logger.info("Notification sent successfully using rumps")
                return
            except Exception as e:
                logger.warning(f"Rumps notification failed: {str(e)}")

            # Method 2: Using osascript (macOS native notifications)
            try:
                logger.debug("Trying osascript notification...")
                script = f"""
                display notification "{message}" with title "{title}" subtitle "{subtitle}"
                """
                subprocess.run(["osascript", "-e", script], check=True)
                logger.info("Notification sent successfully using osascript")
                return
            except Exception as e:
                logger.warning(f"Osascript notification failed: {str(e)}")

            # If all methods fail, show an alert
            logger.error("All notification methods failed")
            rumps.alert(
                "Bildirim Hatası",
                "Bildirim gönderilemedi. Lütfen sistem ayarlarını kontrol edin.",
            )

        except Exception as e:
            logger.error(f"Error in send_notification: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    @rumps.clicked("Bildirim Testi")
    def test_notification(self, _):
        """Test notification functionality"""
        try:
            logger.info("Testing notification system...")
            self.send_notification(
                title="Test Bildirimi",
                subtitle="Başarılı",
                message="Bu bir test bildirimidir. Eğer bu bildirimi görebiliyorsanız, sistem bildirimleri çalışıyor demektir.",
                sound=True,
            )
        except Exception as e:
            logger.error(f"Test notification failed: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

    def start_update_thread(self):
        try:
            self.update_thread = rumps.Timer(
                self.get_new_eq, 60
            )  # Check every 60 seconds
            self.update_thread.start()
            logger.info("Update thread started successfully")
        except Exception as e:
            logger.error(f"Failed to start update thread: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def fetch_all_eqs(self):
        try:
            logger.info("Fetching earthquake data from Koeri")
            response = requests.get("http://www.koeri.boun.edu.tr/scripts/lst4.asp")
            response.raise_for_status()
            eq_raws = [
                line for line in response.text.split("\r\n") if "MARMARA DENIZI" in line
            ]
            eqs = [" ".join(eq_raw.split()).split() for eq_raw in eq_raws]
            logger.info(f"Successfully fetched {len(eqs)} earthquake records")
            return eqs
        except requests.RequestException as e:
            logger.error(f"Network error while fetching earthquake data: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            rumps.alert("Hata", f"Deprem verileri alınamadı: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error while fetching earthquake data: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            rumps.alert("Hata", f"Beklenmeyen bir hata oluştu: {str(e)}")
            return []

    def median(self, lst):
        try:
            n = len(lst)
            s = sorted(lst)
            result = (
                (sum(s[n // 2 - 1 : n // 2 + 1]) / 2.0, s[n // 2])[n % 2] if n else None
            )
            logger.debug(f"Calculated median: {result} from list of length {n}")
            return result
        except Exception as e:
            logger.error(f"Error calculating median: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None

    def format_eq(self, eq):
        try:
            formatted = f"{eq[6]} şiddetinde deprem - {eq[0]} {eq[1]}"
            logger.debug(f"Formatted earthquake data: {formatted}")
            return formatted
        except Exception as e:
            logger.error(f"Error formatting earthquake data: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return "Format hatası"

    def fetch_last_eq(self):
        try:
            eqs = self.fetch_all_eqs()
            if eqs:
                result = self.format_eq(eqs[0])
                logger.info(f"Successfully fetched last earthquake: {result}")
                return result
            logger.warning("No earthquake data available")
            return "Deprem verisi alınamadı"
        except Exception as e:
            logger.error(f"Error fetching last earthquake: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return "Veri alınamadı"

    def fetch_eq_stats(self):
        try:
            eqs = self.fetch_all_eqs()
            if not eqs:
                logger.warning("No earthquake data available for statistics")
                return "İstatistik verisi alınamadı"

            num = len(eqs)
            highest = max(float(eq[6]) for eq in eqs)
            med = self.median([float(eq[6]) for eq in eqs])
            result = f"Son 500 deprem içinde {num} Marmara depremi\nEn yüksek: {highest}, Ortalama: {med}"
            logger.info(f"Successfully calculated earthquake statistics: {result}")
            return result
        except Exception as e:
            logger.error(f"Error calculating earthquake statistics: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return "İstatistik hesaplanamadı"

    def is_new(self, eq):
        try:
            home = os.path.expanduser("~")
            hashfile_path = os.path.join(home, ".config", "latesteqhash")
            cur_hash_result = hashlib.md5(str.encode(eq)).hexdigest()

            if os.path.isfile(hashfile_path):
                with open(hashfile_path, "r") as f:
                    last_hash_result = f.read().strip()
                is_new = last_hash_result != cur_hash_result
                logger.debug(f"Earthquake data comparison - New: {is_new}")
                return is_new
            else:
                logger.info("No previous earthquake hash found, treating as new")
                return True
        except Exception as e:
            logger.error(f"Error checking for new earthquake: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return True
        finally:
            try:
                os.makedirs(os.path.dirname(hashfile_path), exist_ok=True)
                with open(hashfile_path, "w") as f:
                    f.write(cur_hash_result)
                logger.debug("Successfully updated earthquake hash file")
            except Exception as e:
                logger.error(f"Error updating hash file: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")

    @rumps.timer(60)
    def get_new_eq(self, _):
        try:
            logger.debug("Timer triggered - checking for new earthquakes")
            eq = self.fetch_last_eq()
            if self.is_new(eq):
                logger.info(f"New earthquake detected: {eq}")
                self.send_notification(
                    title="Yeni Deprem",
                    subtitle="Marmara Denizi",
                    message=eq,
                    sound=True,
                )
        except Exception as e:
            logger.error(f"Error in get_new_eq: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

    @rumps.clicked("Son Deprem")
    def last_eq_menu(self, _):
        try:
            eq = self.fetch_last_eq()
            logger.info(f"Showing last earthquake: {eq}")
            self.send_notification(
                title="Son Deprem", subtitle="Marmara Denizi", message=eq, sound=False
            )
        except Exception as e:
            logger.error(f"Error in last_eq_menu: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

    @rumps.clicked("Deprem İstatistikleri")
    def eq_stats_menu(self, _):
        try:
            stats = self.fetch_eq_stats()
            logger.info(f"Showing earthquake stats: {stats}")
            self.send_notification(
                title="Deprem İstatistikleri",
                subtitle="Marmara Denizi",
                message=stats,
                sound=False,
            )
        except Exception as e:
            logger.error(f"Error in eq_stats_menu: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    try:
        MarmaraDepremApp().run()
    except Exception as e:
        logger.error(f"Fatal error in main: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

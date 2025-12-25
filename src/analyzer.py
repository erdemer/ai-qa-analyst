import os
import time
import json
import google.generativeai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

load_dotenv()


class ScreenAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key bulunamadı!")

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={"response_mime_type": "application/json"}
        )

    def _upload_to_gemini(self, video_path):
        print(f"Video yükleniyor: {video_path}")
        video_file = genai.upload_file(path=video_path)

        print("Video işleniyor, bekleniyor...")

        while video_file.state.name == "PROCESSING":
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError("Video işleme başarısız.")

        return video_file

    def analyze_video(self, video_path):
        # 1. Videoyu Yükle
        try:
            video_file = self._upload_to_gemini(video_path)
        except Exception as e:
            return {"human_readable_report": f"Video yükleme hatası: {str(e)}", "maestro_yaml": ""}

        prompt = """
        Sen uzman bir QA Otomasyoncususun. Videoyu analiz et.
        Çıktıyı JSON formatında ver:
        1. "human_readable_report": Markdown tablosu (Adım, Eylem, Detay).
        2. "maestro_yaml": Mobile.dev Maestro yaml kodu (appId: com.example, text veya id kullan).

        JSON Şeması:
        { "human_readable_report": "...", "maestro_yaml": "..." }
        """

        max_retries = 3

        for attempt in range(max_retries):
            try:
                print(f"AI Analizi Başlıyor (Deneme {attempt + 1})...")
                response = self.model.generate_content([video_file, prompt])
                return json.loads(response.text)

            except exceptions.ResourceExhausted:
                # 429 Hatası alırsak
                wait_time = 30
                print(f"⚠️ Kota dolu. {wait_time} saniye bekleniyor...")
                time.sleep(wait_time)
                continue

            except Exception as e:
                return {
                    "human_readable_report": f"Beklenmeyen hata: {str(e)}",
                    "maestro_yaml": "# Hata oluştu."
                }

        return {
            "human_readable_report": "Maksimum deneme süresi aşıldı. Lütfen 1 dakika sonra tekrar deneyin.",
            "maestro_yaml": ""
        }
import os
import yt_dlp

def generate_m3u():
    # CNN Türk'ün güncel canlı yayın URL'si veya kalıcı kanal linki
    live_url = "https://www.youtube.com/watch?v=6N8_r2uwLEc"
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    print("CNN Türk canlı yayın akışı çözümleniyor...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(live_url, download=False)
            title = info_dict.get('title', 'CNN Türk Canlı')
            manifest_url = info_dict.get('url')

            if not manifest_url:
                for f in info_dict.get('formats', []):
                    if '.m3u8' in f.get('url', '') or f.get('protocol') == 'm3u8_native':
                        manifest_url = f['url']
                        break

            if manifest_url:
                # M3U İçeriğini Oluştur
                m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-chno="1" tvg-name="CNNTURK" group-title="Haber",CNN TÜRK
{manifest_url}
"""
                # playlist.m3u dosyasına kaydet
                with open("playlist.m3u", "w", encoding="utf-8") as f:
                    f.write(m3u_content)
                
                print("Başarılı: playlist.m3u güncellendi.")
            else:
                print("Hata: m3u8 adresi bulunamadı.")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    generate_m3u()

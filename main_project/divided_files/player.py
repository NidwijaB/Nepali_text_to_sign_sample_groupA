import pygame

def play_clips_with_subtitles(clip_word_pairs, window_size=(640, 360)):
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()

    font = pygame.font.SysFont('Arial', 28, bold=True)
    text_color = (255, 231, 255)
    bg_color = (0, 0, 0)

    for word, clip in clip_word_pairs:
        fps = clip.fps
        frame_gen = clip.iter_frames(fps=fps, dtype="uint8")
        for frame in frame_gen:
            for event in pygame.event.get():
                if event.type in (pygame.QUIT,):
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            surf = pygame.transform.scale(surf, window_size)
            screen.blit(surf, (0, 0))

            subtitle_surface = font.render(word.capitalize(), True, text_color)
            subtitle_bg = pygame.Surface((subtitle_surface.get_width() + 20,
                                          subtitle_surface.get_height() + 10))
            subtitle_bg.fill(bg_color)
            subtitle_bg.set_alpha(150)

            x = (window_size[0] - subtitle_surface.get_width()) // 2
            y = window_size[1] - subtitle_surface.get_height() - 20

            screen.blit(subtitle_bg, (x - 10, y - 5))
            screen.blit(subtitle_surface, (x, y))

            pygame.display.flip()
            clock.tick(fps)

    pygame.quit()

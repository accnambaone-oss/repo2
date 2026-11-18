import json,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'))
from make_project import make_story, suggest_visual
from render import chunks,validate_story,Animator
from art import art_svg
from audio import make_bed

def test_hand_plan_contiguous():
    story=json.loads((root/'examples'/'divide_trap.json').read_text())
    validate_story(story)
    assert len(story['scenes'])==25
    assert story['scenes'][-1]['end']==90

def test_generated_plan_duration():
    story=make_story('A rat fell into a well. The others fought. Find the way out.',duration='105')
    validate_story(story)
    assert abs(story['scenes'][-1]['end']-105)<.001
    assert story['scenes'][-1]['visual']=='escape'

def test_caption_chunks_preserve_all_words():
    text='The people at the top never fight each other'
    assert ' '.join(chunks(text,4))==text

def test_valid_svg_symbols():
    for v in ['well','swarm','feeding','climb','calendar','conflict','countdown','predator','rope','field','chase','diagram','chess','escape','title']:
        s={'visual':v,'accent':'red'}
        assert '<svg' in art_svg(s) and '</svg>' in art_svg(s)

def test_audio_sample_length_and_peak():
    a=make_bed(.5,[{'start':0,'accent':'red'}],sr=24000)
    assert len(a)==12000
    assert max(abs(a))<1

def test_animator_frame_size():
    story=json.loads((root/'examples'/'divide_trap.json').read_text())
    image=Animator(story,180,320).frame(1.0)
    assert image.size==(180,320)


def test_rat_rig_has_independent_articulation():
    from rigs import rigged_rat_svg
    a=rigged_rat_svg(0.0,'neutral')
    b=rigged_rat_svg(0.25,'neutral')
    assert a!=b
    assert 'linearGradient' in a and '<path' in a
    assert '#fc5164' in rigged_rat_svg(0,'red')


def test_motion_engine_frame_changes_and_repeatable():
    story=json.loads((root/'examples'/'active_motion_demo.json').read_text())
    validate_story(story)
    a=Animator(story,180,320)
    f0=a.frame(4.5);f1=a.frame(4.625)
    assert f0.tobytes()!=f1.tobytes()
    _=a.frame(12.0)
    assert f0.tobytes()==a.frame(4.5).tobytes()


def test_offline_hanif_install_with_fake_checkout(tmp_path):
    from install_upstream_skills import install_from_checkout,HANIF_SUBDIR
    src=tmp_path/'checkout';nested=src/HANIF_SUBDIR
    (nested/'lib').mkdir(parents=True)
    (nested/'SKILL.md').write_text('test upstream skill')
    (nested/'lib'/'film.mjs').write_text('export function run(){}')
    (src/'LICENSE').write_text('test MIT license')
    target=tmp_path/'skills'
    where=install_from_checkout(src,target)
    assert (where/'SKILL.md').exists()
    assert (where/'lib'/'film.mjs').exists()
    assert (where/'UPSTREAM_LICENSE').exists()
    import pytest
    with pytest.raises(FileExistsError):install_from_checkout(src,target)

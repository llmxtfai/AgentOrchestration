import sys

import pytest

from src.cli.main import cli


class TestCli:
    def test_deploy_rejects_missing_manifest(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["ao", "deploy", "missing.yml"])

        with pytest.raises(SystemExit) as exc_info:
            cli()

        captured = capsys.readouterr()
        assert exc_info.value.code == 1
        assert "Error: manifest not found: missing.yml" in captured.err
        assert "Deploying agent from manifest" not in captured.out

    def test_deploy_accepts_existing_manifest(self, tmp_path, monkeypatch, capsys):
        manifest = tmp_path / "manifest.yml"
        manifest.write_text("name: example\n")
        monkeypatch.setattr(sys, "argv", ["ao", "deploy", str(manifest)])

        cli()

        captured = capsys.readouterr()
        assert f"Deploying agent from manifest: {manifest}" in captured.out
        assert captured.err == ""


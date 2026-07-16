import os
import tempfile
import unittest

import torch
import torch.nn as nn

from evaluate_saved import load_checkpoint_into_model


class LoadCheckpointIntoModelTest(unittest.TestCase):
    def test_loads_model_state_dict_from_checkpoint_payload(self):
        model = nn.Sequential(nn.Linear(4, 3))
        checkpoint = {"model_state_dict": model.state_dict()}

        with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as handle:
            torch.save(checkpoint, handle.name)
            path = handle.name

        try:
            loaded_model = load_checkpoint_into_model(model, path, device=torch.device("cpu"))
            self.assertIs(loaded_model, model)
            self.assertEqual(model.state_dict()["0.weight"].shape, torch.Size([3, 4]))
        finally:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()

# showcase/showcase/management/commands/celery_tutorial.py
import time
import subprocess
from django.core.management.base import BaseCommand, CommandError

# Import your tasks
from showcase.heavy_tasks import heavy_task
from showcase.light_tasks import light_task
from celery import chain

RABBIT_CONTAINER = "rabbitmq"

def run(cmd):
    """Run a shell command and return (rc, stdout, stderr)."""
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    out, err = proc.communicate()
    return proc.returncode, out.strip(), err.strip()

def list_queues():
    cmd = [
        "docker", "exec", RABBIT_CONTAINER,
        "rabbitmqctl", "list_queues", "name", "messages", "consumers"
    ]
    rc, out, err = run(cmd)
    print("\n$ " + " ".join(cmd))
    if rc == 0:
        print(out or "(no queues)")
    else:
        print("(could not list queues)")
        if err:
            print(err)

class Command(BaseCommand):
    help = "Guided Celery tutorial: lists queues, enqueues light task, chains heavy->light, and loops."

    def add_arguments(self, parser):
        parser.add_argument(
            "--loop",
            type=int,
            default=10,
            help="Number of heavy->light chains to enqueue in the final loop (default: 10).",
        )
        parser.add_argument(
            "--delay",
            type=float,
            default=0.3,
            help="Seconds to sleep between enqueues for visibility (default: 0.3).",
        )

    def handle(self, *args, **opts):
        loop_n = opts["loop"]
        delay_s = opts["delay"]

        print("\n=== Step 1: List queues (baseline) ===")
        list_queues()

        print("\n=== Step 2: Enqueue a LIGHT task ===")
        try:
            r = light_task.delay("hello from tutorial")
            print(f"Enqueued light_task id={r.id}")
        except Exception as e:
            raise CommandError(f"Failed to enqueue light_task: {e}")

        time.sleep(delay_s)

        print("\n=== Step 3: List queues (light queue should have +1 message) ===")
        list_queues()

        print("\n=== Step 4: Start LIGHT worker in another terminal ===")
        print("Run this in a separate terminal:")
        print("  make light_workers")
        print("Open the RabbitMQ UI at http://localhost:15672 for a live view.")
        input("Press ENTER after the light worker is up and consuming... ")

        # Give worker a moment to drain
        time.sleep(1.0)
        print("\nQueues after starting light worker:")
        list_queues()

        print("\n=== Step 5: Enqueue HEAVY -> LIGHT chain ===")
        try:
            job = chain(
                heavy_task.s(5),   # heavy work ~5s
                light_task.s(),    # receives heavy result
            ).delay()
            print(f"Enqueued chain id={job.id}")
        except Exception as e:
            raise CommandError(f"Failed to enqueue chain: {e}")

        print("\n=== Step 6: Start HEAVY worker in another terminal ===")
        print("Run this in a separate terminal:")
        print("  make heavy_workers")
        input("Press ENTER after the heavy worker is up... ")

        # Give heavy worker a moment to pull the job
        time.sleep(1.0)
        print("\nQueues after starting heavy worker (heavy should start draining):")
        list_queues()

        print(f"\n=== Step 7: Enqueue {loop_n}x HEAVY -> LIGHT chains (with small delay) ===")
        enqueued = 0
        for i in range(loop_n):
            try:
                chain(heavy_task.s(2), light_task.s()).delay()
                enqueued += 1
                print(f"  enqueued chain {i+1}/{loop_n}")
            except Exception as e:
                print(f"  enqueue failed at {i+1}: {e}")
            time.sleep(delay_s)

        print(f"\nEnqueued {enqueued}/{loop_n} chains.")
        print("\nFinal queue snapshot:")
        list_queues()

        print("\n=== Tutorial complete ===")
        print("Watch the heavy worker run the first leg, then the light worker finish the chain.")
        print("Now for celery-beats tutorial - goto django admin to set schedule first")
        

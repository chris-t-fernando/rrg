provider "aws" {
	profile = "default"
	region = "us-west-2"
}

variable "ssh_key_private" {
	type = string
	default = "private.key"
}

resource "aws_instance" "jripper" {
	ami = "ami-03d5c68bab01f3496"
	instance_type = "t2.small"
	key_name = "chris2"
	
	tags = {
		project = "rrg-creator"
		
	}
	
	# terraform state does not include changes to remote-exec - eg. python2 vs python3
	# this is really just used to halt execution until the ec2 instance is ready for us to run the playbook against it
	provisioner "remote-exec" {
		#inline = ["curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py",  "sudo python3 get-pip.py --user", "sudo python3 -m pip install --user ansible"]
		inline = ["ls"]

		connection {
			type        = "ssh"
			user        = "ubuntu"
			private_key = "${file(var.ssh_key_private)}"
			host		= "${self.public_ip}"
			
		}
	}
	
	# set the IP address of the new host
	provisioner "local-exec" {
		command = "sed -i 's/##PLACEHOLDER##/${self.public_ip}/g' scraper-config.yaml" 
		
	}
	
	# run the playbook
	provisioner "local-exec" {
		command = "ansible-playbook -u ubuntu -i '${self.public_ip},' --private-key ${var.ssh_key_private} scraper-config.yaml" 
		
	}
	
	# put the placeholder back for next run
	provisioner "local-exec" {
		command = "sed -i 's/${self.public_ip}/##PLACEHOLDER##/g' scraper-config.yaml" 
		
	}
}
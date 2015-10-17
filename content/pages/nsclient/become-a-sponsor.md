Title: Become a sponsor

NSClient++ is a free and open source tool not backed by any commercial entity. 
In fact I don’t even work with NSClient++ so this is a 100% “spare time effort”.

So if you like and use NSClient++ and perhaps even make money from it. The est way to show your appreciation is to become an official sponsor of NSClient++.

The sponsoring program is rather free form so please do let me know what I can provide you and your company and clients.
The sponsoring program has three levels:

<div class="row">
	<div class="col-md-4">
		<div class="panel panel-info">
			<div class="panel-body">
				<div class="text-center">
					<h3>Fans of NSClient++</h3>
				</div>
			</div>
			<div class="panel-body text-center">
				<p class="lead" style="font-size:30px">
					<strong>?</strong>
				</p>
			</div>
			<ul class="list-group list-group-flush text-center">
				<li class="list-group-item">N/A</li>
				<li class="list-group-item">Warm fuzzy feeling</li>
				<li class="list-group-item">N/A</li>
				<li class="list-group-item">Community support</li>
				<li class="list-group-item">N/A</li>
			</ul>
		</div>
	</div>
	<div class="col-md-4">
		<div class="panel panel-info">
			<div class="panel-body">
				<div class="text-center">
					<h3>Silver sponsor</h3>
				</div>
			</div>
			<div class="panel-body text-center">
				<p class="lead" style="font-size:30px">
					<strong>€100</strong>
				</p>
			</div>
			<ul class="list-group list-group-flush text-center">
				<li class="list-group-item">N/A</li>
				<li class="list-group-item">Warm fuzzy feeling</li>
				<li class="list-group-item">Logo on sponsors page</li>
				<li class="list-group-item">Email support</li>
				<li class="list-group-item">1 incident</li>
			</ul>
		</div>
	</div>
	<div class="col-md-4">
		<div class="panel panel-info">
			<div class="panel-body">
				<div class="text-center">
					<h3>Gold sponsor</h3>
				</div>
			</div>
			<div class="panel-body text-center">
				<p class="lead" style="font-size:30px">
					<strong>€1000</strong>
				</p>
			</div>
			<ul class="list-group list-group-flush text-center">
				<li class="list-group-item">N/A</li>
				<li class="list-group-item">Warm fuzzy feeling</li>
				<li class="list-group-item">Logo on every page</li>
				<li class="list-group-item">Email support</li>
				<li class="list-group-item">5 incident</li>
			</ul>
		</div>
	</div>
</div>

Currently the site has just shy of 100.000 page impressions per month and around 20.000-25.000 unique visitors.

# Become a sponsor

If you are interested in becoming a sponsor or have any questions please be contact me using the form below.

<form action="https://fwdform.herokuapp.com/user/e9122444-e6fe-410b-bd4a-39effee64917" method="post">
	<script>
		function setLevel(level) {
			t = '[' + level + ']'
			s = $('#ta').val()
			old = s
			s = s.replace('[level]', t)
			s = s.replace('[fan]', t)
			s = s.replace('[silver]', t)
			s = s.replace('[gold]', t)
			s = s.replace('[other]', t)
			if (old == s) {
				s += "\n P.S. I forgot to say: " + t
			}
			$('#ta').val(s)
		}
	</script>
	<div class="form-group">
		<label for="email">Your email address</label>
		<input name="email" type="email" class="form-control" id="email" placeholder="Your Email">
	</div>
	<div class="form-group">
		<label for="name">Your name</label>
		<input name="name" type="text" class="form-control" id="name" placeholder="Your Name">
	</div>
	<div class="radio">
		<label>
			<input type="radio" name="level" id="levelfan" value="fan" onclick="setLevel('fan')">Fan of NSClient++</input>
		</label>
	</div>
	<div class="radio">
		<label>
			<input type="radio" name="level" id="levelsilver" value="silver" onclick="setLevel('silver')">Silver sponsoring</input>
		</label>
	</div>
	<div class="radio">
		<label>
			<input type="radio" name="level" id="levelgold" value="gold" onclick="setLevel('gold')">Gold sponsoring</input>
		</label>
	</div>
	<div class="radio">
		<label>
			<input type="radio" name="level" id="levelother" value="gold" onclick="setLevel('other')">Other</input>
		</label>
	</div>
	<div class="form-group">
		<label for="ta">Message</label>
		<textarea name="message" class="form-control" id="ta" rows="10">Hello Michael!
NSClient++ is a really wicked application, really love it!

So I am really really interested in sponsoring so could you let me know how I can become [level] sponsor?

		</textarea>
	</div>
	<button type="submit" class="btn btn-default">Send</button>
</form>
